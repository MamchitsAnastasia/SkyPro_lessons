from pathlib import Path

import pytest
from _pytest.capture import CaptureFixture

from src import decorators


@decorators.log()
def divide(a: int, b: int) -> float:
    """Функция получает два аргумента int и выполняет деление первого аргумента на второй"""
    return a / b


def test_log_decorator_stdout_success(capsys: CaptureFixture[str]) -> None:
    """Тестирует декоратор log на функции без ошибки, при выводе логов в консоль"""
    result = divide(6, 3)
    captured = capsys.readouterr()
    assert "divide started. Inputs: (6, 3), {}" in captured.out
    assert "divide ok" in captured.out
    assert result == 2


def test_log_decorator_stdout_error(capsys: CaptureFixture[str]) -> None:
    """Тестирует декоратор log на функции с ошибкой ZeroDivisionError - деления на 0, при выводе логов в консоль"""
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    captured = capsys.readouterr()
    assert "divide started. Inputs: (1, 0), {}" in captured.out
    assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out


def test_log_decorator_file_success(tmp_path: Path) -> None:
    """Тестирует декоратор log на функции без ошибки, при выводе логов в текстовый файл"""
    log_file = tmp_path / "test.log"  # Создание временного файля для логов

    @decorators.log(filename=str(log_file))
    def multiply(a: int, b: int) -> int:
        """Функция получает два аргумента int и выполняет умножение первого аргумента на второй"""
        return a * b

    result = multiply(3, 4)
    log_content = log_file.read_text()  # Чтение содержимого временного файла
    assert result == 12
    assert "multiply started. Inputs: (3, 4), {}" in log_content
    assert "multiply ok" in log_content


def test_log_decorator_file_error(tmp_path: Path) -> None:
    """Тестирует декоратор log на функции с ошибкой TypeError, при выводе логов в текстовый файл"""
    log_file = tmp_path / "error.log"  # Создание временного файля для логов

    @decorators.log(filename=str(log_file))
    def faulty_func() -> None:
        """Функция вызывает ошибку TypeError"""
        raise TypeError("Something went wrong")

    with pytest.raises(TypeError):
        faulty_func()
    log_content = log_file.read_text()  # Чтение содержимого временного файла
    assert "faulty_func started. Inputs: (), {}" in log_content
    assert "faulty_func error: TypeError" in log_content
