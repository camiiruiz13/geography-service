import pytest

from ports.src.main.api.util.paginator import Paginator


class TestPaginator:

    def test_first_page(self):
        result = Paginator.paginate(
            items=list(range(1, 26)),
            page=1,
            page_size=10,
        )

        assert result.data == list(range(1, 11))
        assert result.pagination.totalElements == 25
        assert result.pagination.totalPages == 3
        assert result.pagination.hasNext is True
        assert result.pagination.hasPrevious is False

    def test_last_page(self):
        result = Paginator.paginate(
            items=list(range(1, 26)),
            page=3,
            page_size=10,
        )

        assert result.data == [21, 22, 23, 24, 25]
        assert result.pagination.hasNext is False
        assert result.pagination.hasPrevious is True

    def test_empty_list(self):
        result = Paginator.paginate(
            items=[],
            page=1,
            page_size=10,
        )

        assert result.data == []
        assert result.pagination.totalElements == 0
        assert result.pagination.totalPages == 0

    def test_page_out_of_range(self):
        result = Paginator.paginate(
            items=[1, 2, 3],
            page=5,
            page_size=10,
        )

        assert result.data == []
        assert result.pagination.totalElements == 3

    @pytest.mark.parametrize(
        "page,page_size",
        [(0, 10), (-1, 10), (1, 0), (1, -5)],
    )
    def test_invalid_parameters(self, page, page_size):
        with pytest.raises(ValueError):
            Paginator.paginate(
                items=[1, 2, 3],
                page=page,
                page_size=page_size,
            )