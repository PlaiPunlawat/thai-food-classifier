"""Unit tests for shared food labels (SSOT)."""
import pytest
from src.config.food_names import food_names


@pytest.mark.unit
class TestFoodLabels:
    """Tests for food_names label data integrity."""

    def test_label_count(self):
        """Model has exactly 72 output classes."""
        assert len(food_names) == 72

    def test_ids_sequential(self):
        """IDs must be exactly 0..71 in order (class index)."""
        ids = [entry['id'] for entry in food_names]
        assert ids == list(range(72))

    def test_entries_have_required_fields(self):
        """Every entry has non-empty name_th and name_en."""
        for entry in food_names:
            assert isinstance(entry['name_th'], str)
            assert isinstance(entry['name_en'], str)
            assert len(entry['name_th']) > 0
            assert len(entry['name_en']) > 0

    def test_spot_check_class_38(self):
        """Spot-check: index 38 is ผัดกะเพรา (Phat Kaphrao)."""
        assert food_names[38]['name_th'] == 'ผัดกะเพรา'

    def test_spot_check_class_65(self):
        """Spot-check: index 65 is ฝอยทอง (Golden Egg Yolk Threads)."""
        assert food_names[65]['name_th'] == 'ฝอยทอง'

    def test_names_unique(self):
        """All English and Thai names should be unique."""
        english_names = [f['name_en'] for f in food_names]
        thai_names = [f['name_th'] for f in food_names]
        assert len(english_names) == len(set(english_names))
        assert len(thai_names) == len(set(thai_names))
