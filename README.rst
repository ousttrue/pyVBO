=====
pyVBO
=====

pythonでVBOを便利に処理するライブラリ。

* python3
* array.array('b')で処理する
* 各種モデルフォーマットとの相互変換

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

* File.open
* File.save
