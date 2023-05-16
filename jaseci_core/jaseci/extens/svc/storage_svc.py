from datetime import datetime

from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.file_handler import FileHandler

from libcloud.storage.providers import get_driver
from libcloud.storage.base import StorageDriver, Object, Container

from typing import Iterator


@JsOrc.service(
    name="store",
    config="STORE_CONFIG",
    manifest="STORE_MANIFEST",
    priority=0,
    proxy=True,
)
class StorageService(JsOrc.CommonService):
    def run(self):
        self.app = StorageHandler(self.config["providers"], self.config.get("default"))

        # Testing
        # obj = self.upload(FileHandler.fromPath("test.txt"))
        # self.download(obj["name"])

    def upload(
        self, file: FileHandler, provider: str = None, container: str = None
    ) -> dict:
        provider = self.app.get_storage(provider)
        buffer = file.open(mode="rb", encoding=None, detached=True)

        metadata = {
            "id": file.id,
            "name": file.name,
            "content_type": file.content_type,
            "created": datetime.utcnow().isoformat(),
        }

        # metadata doesn't support empty value
        if file.field:
            metadata["field"] - file.field

        if container:
            container = provider["driver"].get_container(container_name=container)

        obj: Object = provider["driver"].upload_object_via_stream(
            iterator=buffer,
            container=container or provider["container"],
            object_name=file.absolute_name,
            extra={"meta_data": metadata},
        )

        buffer.close()

        return obj.get_cdn_url()

    def download(
        self, file: str, provider: str = None, container: str = None
    ) -> FileHandler:
        provider = self.app.get_storage(provider)

        obj: Object = provider["driver"].get_object(
            container_name=container or provider["container"].name, object_name=file
        )

        temp_file = FileHandler(file)
        temp_file.open(mode="wb", encoding=None)
        for chunk in provider["driver"].download_object_as_stream(obj):
            temp_file.write(chunk)
        temp_file.close()

        return temp_file

    def delete(self, file: str, provider: str = None, container: str = None) -> bool:
        provider = self.app.get_storage(provider)

        obj: Object = provider["driver"].get_object(
            container_name=container or provider["container"].name, object_name=file
        )

        return provider["driver"].delete_object(obj)

    def create_container(self, name: str, provider: str = None) -> Container:
        provider = self.app.get_storage(provider)

        return provider["driver"].create_container(container_name=name)

    def has_container(self, name: str, provider: str = None) -> bool:
        provider = self.app.get_storage(provider)

        return isinstance(
            provider["driver"].get_container(container_name=name), Container
        )

    def delete_container(self, name: str, provider: str = None) -> bool:
        provider = self.app.get_storage(provider)

        return provider["driver"].delete_container(
            provider["driver"].get_container(container_name=name)
        )


class StorageHandler:
    def __init__(self, providers: dict, default: str = None):
        self.default = default
        self.storage = {}

        for key, value in providers.items():
            try:
                driver = get_driver(value["provider"])(**value["credentials"])
                container = driver.get_container(container_name=value["container"])
                self.storage[key] = {
                    "source": value,
                    "driver": driver,
                    "container": container,
                }
                self.storage[key]
            except Exception as e:
                self.storage[key] = {"source": value, "error": str(e)}

    def get_storage(self, provider: str = None) -> StorageDriver:
        if provider:
            return self.storage[provider]
        elif self.default:
            return self.storage[self.default]
