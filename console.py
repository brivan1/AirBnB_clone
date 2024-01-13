<<<<<<< HEAD
=======
#!/usr/bin/python3

"""Module for the entry point of the command interpreter."""

>>>>>>> c4a3e087c224d3ffc0f33a8129df18546be2422b
import cmd
from models.base_model import BaseModel
from models import storage
import re


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def default(self, line):
        """default cmds when nothing else matches"""
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to check for class.syntax()."""
        check = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not check:
            return line
        className = check.group(1)
        methd = check.group(2)
        argu = check.group(3)
        checkIdnArgs = re.search('^"([^"]*)"(?:, (.*))?$', argu)
        if checkIdnArgs:
            id = checkIdnArgs.group(1)
            attrOrDict = checkIdnArgs.group(2)
        else:
            id = argu
            attrOrDict = False

        attrnValue = ""
        if methd == "update" and attrOrDict:
            matchDict = re.search('^({.*})$', attrOrDict)
            if matchDict:
                self.update_dict(className, id, matchDict.group(1))
                return ""
            matchAttrNValue = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attrOrDict)
            if matchAttrNValue:
                attrnValue = (matchAttrNValue.group(
                    1) or "") + " " + (matchAttrNValue.group(2) or "")
        cmd = methd + " " + className + " " + id + " " + attrnValue
        self.onecmd(cmd)
        return cmd

    def do_quit(self, line):
        """Quit command to exit the program"""
        print("goodbye")
        return True

    def do_EOF(self, line):
        """EOF command to exit the program"""
        print("goodbye")
        return True

    def to_help(self):
        print("help is here")

    def emptyline(self):
        pass

    def do_create(self, line):
        """Creates an instance"""
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.clses():
            print("** class doesn't exist **")
        else:
            x = storage.clses()[line]()
            x.save()
            print(x.id)

    def do_show(self, line):
        """Prints the string of an instance"""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            inputs = line.split(' ')
            if inputs[0] not in storage.clses():
                print("** class doesn't exist **")
            elif len(inputs) < 2:
                print("** instance id missing **")
            else:
                key = f"{inputs[0]}.{ inputs[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance with the class name and id"""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            inputs = line.split(' ')
            if inputs[0] not in storage.clses():
                print("** class doesn't exist **")
            elif len(inputs) < 2:
                print("** instance id missing **")
            else:
                key = "f{inputs[0]}.{inputs[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_update(self, line):
        """Updates an instance"""
        if line == "" or line is None:
            print("** class name missing **")
            return

        rege = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        check = re.search(rege, line)
        className = check.group(1)
        id = check.group(2)
        attr = check.group(3)
        value = check.group(4)
        if not check:
            print("** class name missing **")
        elif className not in storage.clses():
            print("** class doesn't exist **")
        elif id is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(className, id)
            if key not in storage.all():
                print("** no instance found **")
            elif not attr:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                convert = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        convert = float
                    else:
                        convert = int
                else:
                    value = value.replace('"', '')
                attr = storage.attributes()[className]
                if attr in attr:
                    value = attr[attr](value)
                elif convert:
                    try:
                        value = convert(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attr, value)
                storage.all()[key].save()

    def do_all(self, line):
        """ retrieve and prints all instances of a class
        """
        if line != "":
            inputs = line.split(' ')
            if inputs[0] not in storage.clses():
                print("** class doesn't exist **")
            else:
                retr = [str(obj) for key, obj in storage.all().items()
                        if type(obj).__name__ == inputs[0]]
                print(retr)
        else:
            nlist = [str(obj) for key, obj in storage.all().items()]
            print(nlist)

    def do_count(self, line):
        """Counts the object of a class.
        """
        inputs = line.split(' ')
        if not inputs[0]:
            print("** class name missing **")
        elif inputs[0] not in storage.clses():
            print("** class doesn't exist **")
        else:
            match = [
                ki for ki in storage.all() if ki.startswith(
                    inputs[0] + '.')]
            print(len(match))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
