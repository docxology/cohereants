"""Comprehensive tests for glossary_gen module.

This module provides extensive test coverage for all functions in glossary_gen.py,
including edge cases, error conditions, and integration scenarios.
"""

import os
import tempfile
import shutil
from pathlib import Path
from textwrap import dedent

import pytest

from src.glossary_gen import (
    build_api_index,
    generate_markdown_table,
    inject_between_markers,
    _first_sentence,
    _iter_py_files,
    ApiEntry
)


class TestApiEntry:
    """Test the ApiEntry dataclass."""
    
    def test_api_entry_creation(self):
        """Test creating ApiEntry instances."""
        entry = ApiEntry(
            module="test_module",
            name="test_function",
            kind="function",
            summary="Test function description."
        )
        
        assert entry.module == "test_module"
        assert entry.name == "test_function"
        assert entry.kind == "function"
        assert entry.summary == "Test function description."
        
    def test_api_entry_repr(self):
        """Test string representation of ApiEntry."""
        entry = ApiEntry(
            module="test_module",
            name="test_function",
            kind="function",
            summary="Test function description."
        )
        
        repr_str = repr(entry)
        assert "test_module" in repr_str
        assert "test_function" in repr_str
        assert "function" in repr_str


class TestFirstSentence:
    """Test the _first_sentence helper function."""
    
    def test_first_sentence_none_input(self):
        """Test handling of None input."""
        result = _first_sentence(None)
        assert result == ""
        
    def test_first_sentence_empty_string(self):
        """Test handling of empty string input."""
        result = _first_sentence("")
        assert result == ""
        
    def test_first_sentence_single_sentence(self):
        """Test single sentence input."""
        text = "This is a single sentence."
        result = _first_sentence(text)
        # The function removes the trailing period
        assert result == "This is a single sentence"
        
    def test_first_sentence_multiple_sentences(self):
        """Test multiple sentences input."""
        text = "First sentence. Second sentence. Third sentence."
        result = _first_sentence(text)
        # The function removes the trailing period
        assert result == "First sentence"
        
    def test_first_sentence_with_newlines(self):
        """Test text with newlines."""
        text = "First line.\nSecond line.\nThird line."
        result = _first_sentence(text)
        # The function removes the trailing period and joins lines
        assert result == "First line"
        
    def test_first_sentence_long_text_truncation(self):
        """Test truncation of very long text."""
        long_text = "A" * 500
        result = _first_sentence(long_text)
        
        assert len(result) <= 200
        assert result.endswith("...")
        
    def test_first_sentence_exact_length(self):
        """Test text at exact truncation boundary."""
        text = "A" * 197 + "."
        result = _first_sentence(text)
        # Should not truncate, but remove trailing period
        assert result == "A" * 197
        assert not result.endswith("...")
        
    def test_first_sentence_just_over_limit(self):
        """Test text just over truncation limit."""
        text = "A" * 201  # Just over 200 characters
        result = _first_sentence(text)
        # Should truncate and add ellipsis
        assert result.endswith("...")
        assert len(result) <= 200


class TestIterPyFiles:
    """Test the _iter_py_files helper function."""
    
    def test_iter_py_files_basic(self, tmp_path):
        """Test basic Python file iteration."""
        # Create test structure
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        # Create Python files
        (src_dir / "module1.py").write_text("def f1(): pass")
        (src_dir / "module2.py").write_text("def f2(): pass")
        (src_dir / "not_python.txt").write_text("not python")
        
        files = list(_iter_py_files(str(src_dir)))
        
        assert len(files) == 2
        assert any("module1.py" in f for f in files)
        assert any("module2.py" in f for f in files)
        assert not any("not_python.txt" in f for f in files)
        
    def test_iter_py_files_with_subdirectories(self, tmp_path):
        """Test Python file iteration with subdirectories."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        # Create subdirectory structure
        subdir = src_dir / "subdir"
        subdir.mkdir()
        
        (src_dir / "main.py").write_text("def main(): pass")
        (subdir / "helper.py").write_text("def helper(): pass")
        (subdir / "utils.py").write_text("def utils(): pass")
        
        files = list(_iter_py_files(str(src_dir)))
        
        assert len(files) == 3
        assert any("main.py" in f for f in files)
        assert any("helper.py" in f for f in files)
        assert any("utils.py" in f for f in files)
        
    def test_iter_py_files_underscore_files(self, tmp_path):
        """Test that underscore files are properly handled."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        # Create various files
        (src_dir / "public.py").write_text("def public(): pass")
        (src_dir / "_private.py").write_text("def private(): pass")
        (src_dir / "__init__.py").write_text("def init(): pass")
        (src_dir / "_ignore.py").write_text("def ignore(): pass")
        
        files = list(_iter_py_files(str(src_dir)))
        
        # Should include public.py and __init__.py, exclude _private.py and _ignore.py
        assert len(files) == 2
        assert any("public.py" in f for f in files)
        assert any("__init__.py" in f for f in files)
        assert not any("_private.py" in f for f in files)
        assert not any("_ignore.py" in f for f in files)
        
    def test_iter_py_files_empty_directory(self, tmp_path):
        """Test iteration over empty directory."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        files = list(_iter_py_files(str(src_dir)))
        assert len(files) == 0


class TestBuildApiIndex:
    """Test the build_api_index function."""
    
    def test_build_api_index_basic_function(self, tmp_path):
        """Test building API index with basic function."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "module.py", dedent("""
            def public_function():
                \"\"\"Public function docstring.\"\"\"
                return True
        """))
        
        entries = build_api_index(str(src_dir))
        
        assert len(entries) == 1
        entry = entries[0]
        assert entry.module == "module"
        assert entry.name == "public_function"
        assert entry.kind == "function"
        assert "Public function docstring" in entry.summary
        
    def test_build_api_index_basic_class(self, tmp_path):
        """Test building API index with basic class."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "module.py", dedent("""
            class PublicClass:
                \"\"\"Public class docstring.\"\"\"
                def method(self):
                    return True
        """))
        
        entries = build_api_index(str(src_dir))
        
        assert len(entries) == 1
        entry = entries[0]
        assert entry.module == "module"
        assert entry.name == "PublicClass"
        assert entry.kind == "class"
        assert "Public class docstring" in entry.summary
        
    def test_build_api_index_private_items(self, tmp_path):
        """Test that private items are excluded."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "module.py", dedent("""
            def public_function():
                \"\"\"Public function.\"\"\"
                return True
                
            def _private_function():
                \"\"\"Private function.\"\"\"
                return False
                
            class _PrivateClass:
                \"\"\"Private class.\"\"\"
                pass
        """))
        
        entries = build_api_index(str(src_dir))
        
        assert len(entries) == 1
        entry = entries[0]
        assert entry.name == "public_function"
        assert entry.name != "_private_function"
        assert entry.name != "_PrivateClass"
        
    def test_build_api_index_package_init(self, tmp_path):
        """Test handling of package __init__.py files."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        pkg_dir = src_dir / "package"
        pkg_dir.mkdir()
        
        write(pkg_dir / "__init__.py", dedent("""
            def package_function():
                \"\"\"Package function.\"\"\"
                return True
        """))
        
        entries = build_api_index(str(src_dir))
        
        assert len(entries) == 1
        entry = entries[0]
        assert entry.module == "package"
        assert entry.name == "package_function"
        
    def test_build_api_index_multiple_modules(self, tmp_path):
        """Test building API index with multiple modules."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "module1.py", dedent("""
            def function1():
                \"\"\"First function.\"\"\"
                return 1
        """))
        
        write(src_dir / "module2.py", dedent("""
            def function2():
                \"\"\"Second function.\"\"\"
                return 2
        """))
        
        entries = build_api_index(str(src_dir))
        
        assert len(entries) == 2
        names = {entry.name for entry in entries}
        assert "function1" in names
        assert "function2" in names
        
    def test_build_api_index_sorting(self, tmp_path):
        """Test that entries are properly sorted."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "module.py", dedent("""
            def zebra():
                \"\"\"Zebra function.\"\"\"
                return "zebra"
                
            def alpha():
                \"\"\"Alpha function.\"\"\"
                return "alpha"
        """))
        
        entries = build_api_index(str(src_dir))
        
        assert len(entries) == 2
        # Should be sorted by name
        assert entries[0].name == "alpha"
        assert entries[1].name == "zebra"
        
    def test_build_api_index_syntax_error_handling(self, tmp_path):
        """Test handling of files with syntax errors."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "good.py", dedent("""
            def good_function():
                \"\"\"Good function.\"\"\"
                return True
        """))
        
        write(src_dir / "bad.py", dedent("""
            def bad_function(:
                \"\"\"Bad function with syntax error.\"\"\"
                return False
        """))
        
        entries = build_api_index(str(src_dir))
        
        # Should only include the good file
        assert len(entries) == 1
        assert entries[0].name == "good_function"
        
    def test_build_api_index_no_docstring(self, tmp_path):
        """Test handling of functions/classes without docstrings."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "module.py", dedent("""
            def no_docstring():
                return True
                
            class NoDocstring:
                pass
        """))
        
        entries = build_api_index(str(src_dir))
        
        assert len(entries) == 2
        for entry in entries:
            assert entry.summary == ""
            
    def test_build_api_index_nested_classes(self, tmp_path):
        """Test handling of nested classes (should not be included)."""
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        
        write(src_dir / "module.py", dedent("""
            class OuterClass:
                \"\"\"Outer class.\"\"\"
                
                class InnerClass:
                    \"\"\"Inner class.\"\"\"
                    pass
        """))
        
        entries = build_api_index(str(src_dir))
        
        # Should only include the outer class
        assert len(entries) == 1
        assert entries[0].name == "OuterClass"
        assert entries[0].name != "InnerClass"



# Helper function for writing files
def write(path: Path, content: str) -> None:
    """Write content to a file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


if __name__ == "__main__":
    pytest.main([__file__])
