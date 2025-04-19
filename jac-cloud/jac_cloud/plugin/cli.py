"""Module for registering CLI plugins for jaseci."""

from getpass import getpass
from os import getenv
from os.path import split
from pickle import load
from typing import Any

from jaclang.cli.cmdreg import cmd_registry
from jaclang.runtimelib.context import ExecutionContext
from jaclang.runtimelib.feature import JacFeature, JacProgram, hookimpl

from pymongo.errors import ConnectionFailure, OperationFailure

from ..core.architype import BulkWrite, NodeAnchor
from ..core.context import PUBLIC_ROOT_ID, SUPER_ROOT_ID
from ..jaseci.datasources import Collection
from ..jaseci.models import User as BaseUser
from ..jaseci.utils import logger


class JacCmd:
    """Jac CLI."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Create Jac CLI cmds."""

        @cmd_registry.register
        def serve(filename: str, host: str = "0.0.0.0", port: int = 8000) -> None:
            from jaclang import JacFeature as Jac
            from jac_cloud import FastAPI

            """Serve the jac application."""
            base, mod = split(filename)
            base = base if base else "./"
            mod = mod[:-4]

            FastAPI.enable()
            jctx = ExecutionContext.create()

            if filename.endswith(".jac"):
                Jac.jac_import(
                    target=mod,
                    base_path=base,
                    cachable=True,
                    override_name="__main__",
                )
            elif filename.endswith(".jir"):
                with open(filename, "rb") as f:
                    JacFeature(base).attach_program(
                        JacProgram(mod_bundle=load(f), bytecode=None, sem_ir=None)
                    )
                    Jac.jac_import(
                        target=mod,
                        base_path=base,
                        cachable=True,
                        override_name="__main__",
                    )
            else:
                jctx.close()
                JacFeature.detach_machine()
                raise ValueError("Not a valid file!\nOnly supports `.jac` and `.jir`")

            FastAPI.start(host=host, port=port)

            jctx.close()
            JacFeature.detach_machine()

        @cmd_registry.register
        def create_system_admin(
            filename: str, email: str = "", password: str = ""
        ) -> str:
            from jaclang import JacFeature as Jac

            if not getenv("DATABASE_HOST"):
                raise NotImplementedError(
                    "DATABASE_HOST env-var is required for this API!"
                )

            base, mod = split(filename)
            base = base if base else "./"
            mod = mod[:-4]

            if filename.endswith(".jac"):
                Jac.jac_import(
                    target=mod,
                    base_path=base,
                    cachable=True,
                    override_name="__main__",
                )
            elif filename.endswith(".jir"):
                with open(filename, "rb") as f:
                    JacFeature(base).attach_program(
                        JacProgram(mod_bundle=load(f), bytecode=None, sem_ir=None)
                    )
                    Jac.jac_import(
                        target=mod,
                        base_path=base,
                        cachable=True,
                        override_name="__main__",
                    )

            if not email:
                trial = 0
                while (email := input("Email: ")) != input("Confirm Email: "):
                    if trial > 2:
                        raise ValueError("Email don't match! Aborting...")
                    print("Email don't match! Please try again.")
                    trial += 1

            if not password:
                trial = 0
                while (password := getpass()) != getpass(prompt="Confirm Password: "):
                    if trial > 2:
                        raise ValueError("Password don't match! Aborting...")
                    print("Password don't match! Please try again.")
                    trial += 1

            user_model = BaseUser.model()
            user_request = user_model.register_type()(
                email=email,
                password=password,
                **user_model.system_admin_default(),
            )

            Collection.apply_indexes()
            with user_model.Collection.get_session() as session, session.start_transaction():
                req_obf: dict = user_request.obfuscate()
                req_obf.update(
                    {
                        "root_id": SUPER_ROOT_ID,
                        "is_activated": True,
                        "is_admin": True,
                    }
                )

                retry = 0
                while True:
                    try:
                        default_data: dict[str, Any] = {
                            "name": None,
                            "root": None,
                            "access": {
                                "all": "NO_ACCESS",
                                "roots": {"anchors": {}},
                            },
                            "architype": {},
                            "edges": [],
                        }

                        if not NodeAnchor.Collection.find_by_id(
                            PUBLIC_ROOT_ID, session=session
                        ):
                            NodeAnchor.Collection.insert_one(
                                {"_id": PUBLIC_ROOT_ID, **default_data},
                                session=session,
                            )
                        if not NodeAnchor.Collection.find_by_id(
                            SUPER_ROOT_ID, session=session
                        ):
                            NodeAnchor.Collection.insert_one(
                                {"_id": SUPER_ROOT_ID, **default_data},
                                session=session,
                            )
                        if id := (
                            user_model.Collection.insert_one(req_obf, session=session)
                        ).inserted_id:
                            BulkWrite.commit(session)
                            return f"System Admin created with id: {id}"
                        raise SystemError("Can't create System Admin!")
                    except (ConnectionFailure, OperationFailure) as ex:
                        if (
                            ex.has_error_label("TransientTransactionError")
                            and retry <= BulkWrite.SESSION_MAX_TRANSACTION_RETRY
                        ):
                            retry += 1
                            logger.error(
                                "Error executing bulk write! "
                                f"Retrying [{retry}/{BulkWrite.SESSION_MAX_TRANSACTION_RETRY}] ..."
                            )
                            continue
                        logger.exception(
                            f"Error executing bulk write after max retry [{BulkWrite.SESSION_MAX_TRANSACTION_RETRY}] !"
                        )
                        raise
                    except Exception:
                        logger.exception("Error executing bulk write!")
                        raise

            raise Exception("Can't process registration. Please try again!")
