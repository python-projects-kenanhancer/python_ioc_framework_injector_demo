import time
from typing import NewType

from injector import Binder, Injector, Module, multiprovider, provider

Name = NewType("Name", str)
Description = NewType("Description", str)
Names = NewType("Names", list[str])


class MyModule(Module):
    def configure(self, binder: Binder):
        binder.bind(Name, to="Sherlock")

    @provider
    def provide_description(self) -> Description:
        return Description("A man of astounding insight (at %s)" % time.time())

    @multiprovider
    def provide_names_v1(self) -> list[Name]:
        return [Name("kenan"), Name("enes"), Name("eren")]

    @multiprovider
    def provide_names_v2(self) -> Names:
        return Names(["kenan", "enes", "eren"])


if __name__ == "__main__":
    injector = Injector([MyModule])

    name = injector.get(Name)
    description = injector.get(Description)
    names_v1 = injector.get(list[Name])
    names_v2 = injector.get(Names)

    print(name, description)
