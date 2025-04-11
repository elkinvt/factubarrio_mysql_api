from flask_restful import Resource
from flask import request
from flask_cors import cross_origin
from src.models.productos import Productos
from src.models import to_dict
import traceback

class ProductosApi(Resource):
    @cross_origin
    def post(self):
            print("Entró al método POST de ProductosApi")  # <- Primera marca
            try:
                # 1. Obtener el JSON recibido
                data = request.get_json()
                print("JSON recibido:", data)
                
                # 2. Crear el producto con los datos enviados
                producto = Productos(
                                    codigo=data.get('codigoProducto'),
                                    nombre=data.get('nombreProducto', "").capitalize(),
                                    descripcion=data.get('descripcionProducto', "").capitalize(),
                                    categoria_idcategoria=data.get('categoriaProducto'),
                                    precio_unitario=float(data.get('precioProducto', 0)),
                                    unidad_medida_idunidad_medida=data.get('unidadMedidaProducto'),
                                    presentacion=str(data.get('presentacionProducto', "")),
                                    cantidad_stock=int(data.get('cantidadStockProducto', 0))
                                    
                )
            
                producto_guardado = Productos.agregar_producto(producto)
                
                return{
                    "mensaje": "producto almacenado correctamente",
                    "producto": producto.to_dict(producto_guardado)
                },201
            except Exception as e:
                print("Error al crear producto:", e)
                traceback.print_exc()
                return{"error: str(e)"}, 500
                
            
            
            

            
            
