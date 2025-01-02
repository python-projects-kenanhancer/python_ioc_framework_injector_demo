from typing import NewType

from injector import Binder, Injector, Module

Name = NewType("Name", str)
Description = NewType("Description", str)


class MyModule(Module):
    def configure(self, binder: Binder):
        binder.bind(Name, to="Sherlock")
        binder.bind(Description, to="A man of astounding insight")


if __name__ == "__main__":
    injector = Injector([MyModule])

    name = injector.get(Name)
    description = injector.get(Description)

    print(name, description)
