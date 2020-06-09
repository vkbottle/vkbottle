import typing
from .base import Uploader
from io import BytesIO


class DocUploader(Uploader):
    FILE_EXTENSIONS = [
        ".txt",
        ".docx",
        ".mp3",
    ]

    async def upload_doc_to_wall(
        self, pathlike: typing.Union[str, BytesIO], group_id: int = None, **params
    ) -> typing.Union[str, dict]:
        server = await self.api.request(
            "docs.getWallUploadServer", {"group_id": group_id} if group_id else {}
        )
        uploader = await self.upload(
            server, {"file": self.open_pathlike(pathlike)}, params
        )
        params = {**uploader, **params}
        doc = await self.api.request("docs.save", params)
        if self.gas:
            doc = doc[doc["type"]]
            return self.generate_attachment_string("doc", doc["owner_id"], doc["id"])
        return doc

    async def upload_doc(
        self, pathlike: typing.Union[str, BytesIO], group_id: int = None, **params
    ) -> typing.Union[str, dict]:
        server = await self.api.request(
            "docs.getUploadServer", {"group_id": group_id} if group_id else {}
        )
        uploader = await self.upload(
            server, {"file": self.open_pathlike(pathlike)}, params
        )
        params = {**uploader, **params}
        doc = await self.api.request("docs.save", params)
        if self.gas:
            doc = doc[doc["type"]]
            return self.generate_attachment_string("doc", doc["owner_id"], doc["id"])
        return doc

    async def upload_doc_to_message(
        self,
        pathlike: typing.Union[str, BytesIO],
        peer_id: int,
        doc_type: str = "doc",
        **params
    ):
        server = await self.api.request(
            "docs.getMessagesUploadServer", {"type": doc_type, "peer_id": peer_id}
        )
        uploader = await self.upload(
            server, {"file": self.open_pathlike(pathlike)}, params
        )
        params = {**uploader, **params}
        doc = await self.api.request("docs.save", params)
        if self.gas:
            doc = doc[doc["type"]]
            return self.generate_attachment_string("doc", doc["owner_id"], doc["id"])
        return doc
