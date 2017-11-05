import pathlib
from renderer import AttributeLayout, Semantics, ShaderProgram


class Gizmo:
    VS = (pathlib.Path(__file__).parent / 'gizmo.vert').read_text()
    FS = (pathlib.Path(__file__).parent / 'gizmo.frag').read_text()
    vertex_layout = (
        AttributeLayout(Semantics.POSITION, 'f', 3),
        AttributeLayout(Semantics.NORMAL, 'f', 3),
        AttributeLayout(Semantics.COLOR, 'f', 4),
        AttributeLayout(Semantics.TEXCOORD, 'f', 2)
    )
GizmoShader = ShaderProgram(Gizmo.VS, Gizmo.FS, Gizmo.vertex_layout)


MmdShader = ShaderProgram(
    (pathlib.Path(__file__).parent / 'mmd.vert').read_text(),
    (pathlib.Path(__file__).parent / 'mmd.frag').read_text(),
    vertex_layout=(
        AttributeLayout(Semantics.POSITION, 'f', 3),
        AttributeLayout(Semantics.NORMAL, 'f', 3),
        AttributeLayout(Semantics.TEXCOORD, 'f', 2)
    ),
    vertex_stride = 38
)
