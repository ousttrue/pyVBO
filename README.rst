=====
pyVBO
=====

pythonでVBOを便利に処理するライブラリ。

* python3
* array.arrayもしくはctypes.Arrayでバッファを構築する
* 各種モデルフォーマットとの相互変換
* typingの実験

::

    import pyvbo

    vertex_data=pyvbo.load_from_obj('teepot.obj')
    vbo=pyvbo.vbo.create(vertex_data)
    
    vbo.begin()
    for submesh in vbo.submeshes:
        shader.set_material(submesh.material)    
        submesh.draw()

ToDo
====

* VertexList
* MaterialList
* Shader Selector
* BoundingBox
* Bone gizmo
* Transform gizmo

