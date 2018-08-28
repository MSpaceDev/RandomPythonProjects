from abc import ABC, abstractmethod

from jawa.constants import *
from jawa.util.descriptor import method_descriptor

import six.moves

def class_from_invokedynamic(ins, cf):
    """
    Gets the class type for an invokedynamic instruction that
    calls a constructor.
    """
    const = ins.operands[0]
    bootstrap = cf.bootstrap_methods[const.method_attr_index]
    method = cf.constants.get(bootstrap.method_ref)
    # Make sure this is a reference to LambdaMetafactory
    assert method.reference_kind == 6 # REF_invokeStatic
    assert method.reference.class_.name.value == "java/lang/invoke/LambdaMetafactory"
    assert method.reference.name_and_type.name.value == "metafactory"
    assert len(bootstrap.bootstrap_args) == 3 # Num arguments
    # Now check the arguments.  Note that LambdaMetafactory has some
    # arguments automatically filled in.
    methodhandle = cf.constants.get(bootstrap.bootstrap_args[1])
    assert methodhandle.reference_kind == 8 # REF_newInvokeSpecial
    assert methodhandle.reference.name_and_type.name.value == "<init>"
    # OK, now that we've done all those checks, just get the type
    # from the constructor.
    return methodhandle.reference.class_.name.value

class WalkerCallback(ABC):
    """
    Interface for use with walk_method.

    Any of the methods may raise StopIteration to signal the end of checking
    instructions.
    """

    @abstractmethod
    def on_new(self, ins, const):
        """
        Called for a `new` instruction.

        ins: The instruction
        const: The constant, a ConstantClass

        return value: what to put on the stack
        """
        pass

    @abstractmethod
    def on_invoke(self, ins, const, obj, args):
        """
        Called when a method is invoked.

        ins: The instruction
        const: The constant, either a MethodReference or InterfaceMethodRef
        obj: The object being invoked on (or null for a static method)
        args: The arguments to the method, popped from the stack

        return value: what to put on the stack (for a non-void method)
        """
        pass

    @abstractmethod
    def on_get_field(self, ins, const, obj):
        """
        Called for a getfield or getstatic instruction.

        ins: The instruction
        const: The constant, a FieldReference
        obj: The object to get from, or None for a static field

        return value: what to put on the stack
        """
        pass

    @abstractmethod
    def on_put_field(self, ins, const, obj, value):
        """
        Called for a putfield or putstatic instruction.

        ins: The instruction
        const: The constant, a FieldReference
        obj: The object to store into, or None for a static field
        value: The value to assign
        """
        pass

def walk_method(cf, method, callback, verbose):
    assert isinstance(callback, WalkerCallback)

    stack = []
    locals = {}
    for ins in method.code.disassemble():
        if ins.mnemonic in ("bipush", "sipush"):
            stack.append(ins.operands[0].value)
        elif ins.mnemonic.startswith("fconst"):
            stack.append(float(ins.mnemonic[-1]))
        elif ins.mnemonic == "aconst_null":
            stack.append(None)
        elif ins.mnemonic in ("ldc", "ldc_w"):
            const = ins.operands[0]

            if isinstance(const, ConstantClass):
                stack.append("%s.class" % const.name.value)
            elif isinstance(const, String):
                stack.append(const.string.value)
            else:
                stack.append(const.value)
        elif ins.mnemonic == "new":
            const = ins.operands[0]

            try:
                stack.append(callback.on_new(ins, const))
            except StopIteration:
                break
        elif ins.mnemonic in ("getfield", "getstatic"):
            const = ins.operands[0]
            if ins.mnemonic != "getstatic":
                obj = stack.pop()
            else:
                obj = None

            try:
                stack.append(callback.on_get_field(ins, const, obj))
            except StopIteration:
                break
        elif ins.mnemonic in ("putfield", "putstatic"):
            const = ins.operands[0]
            value = stack.pop()
            if ins.mnemonic != "putstatic":
                obj = stack.pop()
            else:
                obj = None

            try:
                callback.on_put_field(ins, const, obj, value)
            except StopIteration:
                break
        elif ins.mnemonic in ("invokevirtual", "invokespecial", "invokeinterface", "invokestatic"):
            const = ins.operands[0]
            method_desc = const.name_and_type.descriptor.value
            desc = method_descriptor(method_desc)
            num_args = len(desc.args)

            args = []

            for i in six.moves.range(num_args):
                args.insert(0, stack.pop())
            if ins.mnemonic != "invokestatic":
                obj = stack.pop()
            else:
                obj = None

            try:
                ret = callback.on_invoke(ins, const, obj, args)
            except StopIteration:
                break
            if desc.returns.name != "void":
                stack.append(ret)
        elif ins.mnemonic == "astore":
            locals[ins.operands[0].value] = stack.pop()
        elif ins.mnemonic == "aload":
            stack.append(locals[ins.operands[0].value])
        elif ins.mnemonic == "dup":
            stack.append(stack[-1])
        elif ins.mnemonic in ("checkcast", "return"):
            pass
        elif verbose:
            print("Unknown instruction %s: stack is %s" % (ins, stack))
