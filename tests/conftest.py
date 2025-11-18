import pytest
from django.conf import settings


@pytest.fixture(autouse=True, scope="session")
def _temp_media_root(tmp_path_factory):
    """Use a temporary MEDIA_ROOT for the whole test session.

    - Prevents test uploads from polluting the real media/.
    - tmp_path_factory creates an isolated temp directory and removes it
      after the test session ends.
    """
    tmp_media = tmp_path_factory.mktemp("media")
    settings.MEDIA_ROOT = str(tmp_media)
    yield
    # No manual cleanup is needed: pytest handles tmp dirs lifecycle.
