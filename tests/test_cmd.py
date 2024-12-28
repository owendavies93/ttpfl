import pytest
from unittest.mock import patch, MagicMock

from ttpfl.cmd import run_model, execute_command

@pytest.fixture
def sample_data():
    return {
        'players': ['Player1', 'Player2', 'Player3'],
        'points': [10, 20, 30],
        'prices': [1000, 2000, 3000],
        'tours': [1, 1, 1],
        'current_picks': [],
        'already_picked': []
    }

@pytest.fixture
def mock_model():
    with patch('ttpfl.model.run_model') as mock:
        mock.return_value = (15000, [MagicMock(value=lambda: 1), MagicMock(value=lambda: 0), MagicMock(value=lambda: 1)])
        yield mock

@pytest.fixture
def mock_data():
    with patch('ttpfl.data') as mock:
        mock.get_player_id.return_value = 0
        mock.save_state.return_value = None
        yield mock

def test_run_model(sample_data, mock_model, capsys):
    run_model(**sample_data)
    captured = capsys.readouterr()
    
    assert "Picked players:" in captured.out
    assert "Best remaining players:" in captured.out
    assert "Budget remaining: 15000" in captured.out
    mock_model.assert_called_once()

@patch('builtins.input')
def test_execute_command_run(mock_input, sample_data, mock_model, mock_data, capsys):
    mock_input.return_value = "run"
    
    execute_command(**sample_data)
    
    captured = capsys.readouterr()
    assert "Picked players:" in captured.out
    mock_model.assert_called_once()

@patch('builtins.input')
@patch('ttpfl.cmd.prompt')
def test_execute_command_pick_player(mock_prompt, mock_input, sample_data, mock_model, mock_data, capsys):
    mock_input.return_value = "p"
    mock_prompt.return_value = "Player1"
    
    current_picks, _ = execute_command(**sample_data)
    
    captured = capsys.readouterr()
    assert "Picking Player1" in captured.out
    assert 0 in current_picks
    
    current_picks, _ = execute_command(
        players=sample_data['players'],
        points=sample_data['points'],
        prices=sample_data['prices'],
        tours=sample_data['tours'],
        current_picks=current_picks,
        already_picked=[]
    )
    
    captured = capsys.readouterr()
    assert "Player Player1 already picked" in captured.out
    assert current_picks.count(0) == 1

    mock_input.return_value = "p"
    mock_prompt.return_value = "Player100"

    current_picks, _ = execute_command(**sample_data)
    captured = capsys.readouterr()
    assert "Player Player100 not found" in captured.out

@patch('builtins.input')
@patch('ttpfl.cmd.prompt')
def test_execute_command_remove_player(mock_prompt, mock_input, sample_data, mock_model, mock_data, capsys):
    mock_input.return_value = "rm"
    mock_prompt.return_value = "Player1"
    
    _, already_picked = execute_command(**sample_data)
    
    captured = capsys.readouterr()
    assert "Removing Player1" in captured.out
    assert 0 in already_picked
    
@patch('builtins.input')
def test_execute_command_show(mock_input, sample_data, mock_data, capsys):
    mock_input.return_value = "show"
    sample_data['current_picks'] = [0]
    
    execute_command(**sample_data)
    
    captured = capsys.readouterr()
    assert "Current picks:" in captured.out
    assert "Player1" in captured.out

@patch('builtins.input')
def test_execute_command_clear(mock_input, sample_data, mock_data):
    mock_input.return_value = "clear"
    sample_data['current_picks'] = [0]
    sample_data['already_picked'] = [1]
    
    current_picks, already_picked = execute_command(**sample_data)
    
    assert len(current_picks) == 0
    assert len(already_picked) == 0

@patch('builtins.input')
def test_execute_command_invalid(mock_input, sample_data, mock_data, capsys):
    mock_input.return_value = ""
    
    execute_command(**sample_data)
    
    captured = capsys.readouterr()
    assert "Invalid command" in captured.out

@patch('builtins.input')
def test_execute_command_exit(mock_input, sample_data, mock_data):
    mock_input.return_value = "exit"
    
    with pytest.raises(SystemExit):
        execute_command(**sample_data) 
