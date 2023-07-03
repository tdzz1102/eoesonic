from pathlib import Path


base_path = Path(__file__).parent.parent


class Config:
    db_file_path = base_path / 'database.db'
    music_path = base_path / 'Data' / 'music'
