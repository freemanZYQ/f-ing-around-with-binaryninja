from __future__ import annotations

from collections import deque

from binaryninja import MediumLevelILBasicBlock, MediumLevelILInstruction

from . import mlil_ast

print(dir(mlil_ast))

class MediumLevelILAstNode(object):
    def __init__(self, ast: mlil_ast.MediumLevelILAst):
        self._children = deque()
        self._ast = ast

    def prepend(self, child: MediumLevelILAstNode):
        self._children.appendleft(child)

    def append(self, child: MediumLevelILAstNode):
        self._children.append(child)

    @property
    def children(self) -> list:
        return list(self._children)

    @property
    def ast(self) -> mlil_ast.MediumLevelILAst:
        return self._ast


class MediumLevelILAstSeqNode(MediumLevelILAstNode):
    def __init__(self, ast: mlil_ast.MediumLevelILAst, header: MediumLevelILBasicBlock):
        if not isinstance(header, MediumLevelILBasicBlock):
            raise TypeError(
                f"header should be a MediumLevelILBasicBlock, got {type(header)}"
            )
        super().__init__(ast)
        self._header = header

    @property
    def start(self):
        return self._header.start

    @property
    def header(self):
        return self._header

    def __str__(self):
        return f"<seq: header={self._header}, {len(self.children)} children>"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self.header == other.header

    def __hash__(self):
        return hash(self.header)


class MediumLevelILAstCondNode(MediumLevelILAstNode):
    def __init__(self, ast: mlil_ast.MediumLevelILAst, condition: MediumLevelILInstruction):
        self._condition = condition
        super().__init__(ast)

    @property
    def condition(self) -> MediumLevelILInstruction:
        return self._condition

    def __repr__(self):
        return f"<cond: {self.condition}, {len(self.children)} children>"

    def __getitem__(self, key):
        if key:
            return self._children[0]
        else:
            return self._children[1]


class MediumLevelILAstLoopNode(MediumLevelILAstNode):
    pass


class MediumLevelILAstSwitchNode(MediumLevelILAstNode):
    pass


class MediumLevelILAstBasicBlockNode(MediumLevelILAstNode):
    def __init__(self, ast: mlil_ast.MediumLevelILAst, bb: MediumLevelILBasicBlock):
        super().__init__(ast)
        self._bb = bb

    @property
    def block(self) -> MediumLevelILBasicBlock:
        return self._bb

    @property
    def start(self) -> int:
        return self._bb.start

    def __eq__(self, other):
        if isinstance(other, MediumLevelILBasicBlock):
            return self.block == other

        if not isinstance(other, type(self)):
            return False

        return self.block == other.block

    def __hash__(self):
        return hash(self.block)

    def __repr__(self):
        return f"<bb block={self.block}>"