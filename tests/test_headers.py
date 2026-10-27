import pytest

from dagster_mcp import server


class TestBuildHeaders:
    def test_no_token(self):
        headers = server._build_headers("", "")
        assert headers == {}

    def test_with_token(self):
        headers = server._build_headers("my-token", "")
        assert headers == {"Dagster-Cloud-Api-Token": "my-token"}

    def test_extra_headers_valid(self):
        headers = server._build_headers(
            "", '{"Authorization": "Bearer abc", "X-Custom": "val"}'
        )
        assert headers == {"Authorization": "Bearer abc", "X-Custom": "val"}

    def test_extra_headers_merged_with_token(self):
        headers = server._build_headers("my-token", '{"X-Custom": "val"}')
        assert headers == {
            "Dagster-Cloud-Api-Token": "my-token",
            "X-Custom": "val",
        }

    def test_extra_headers_malformed_json(self):
        with pytest.raises(RuntimeError, match="valid JSON object"):
            server._build_headers("", "{not valid json}")

    def test_extra_headers_not_a_dict(self):
        with pytest.raises(RuntimeError, match="must be a JSON object"):
            server._build_headers("", '["a", "b"]')

    def test_extra_headers_non_string_values(self):
        with pytest.raises(RuntimeError, match="must be strings"):
            server._build_headers("", '{"key": 123}')
