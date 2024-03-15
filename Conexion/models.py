from django.db import models

# Create your models here.
class Usuarios(models.Model):
    
    id= models.IntegerField(primary_key=True, serialize=False)
    nombre_usuario=models.CharField(max_length=200,blank=False)
    apellido_usuario=models.CharField(max_length=200,blank=False)
    fecha_nacimiento=models.DateField("Fecha Nacimiento")
    user_name=models.CharField(max_length=100,blank=False,unique=True)
    correo=models.EmailField(blank=True)
    ultima_conexion=models.DateTimeField("fecha ultma conexion")
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Usuarios"
               

    
    

class TiposGastos(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    nombre_tipo_gasto=models.CharField(max_length=200,blank=False,unique=True)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="TiposGastos"
               

    def __str__(self):
        return (f"{self.nombre_tipo_gasto.capitalize()} , {self.nombre_tipo_gasto.capitalize()}")
    
class CategoriaGastos(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    nombre_categoria=models.CharField(max_length=200,blank=False)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="CategoriaGastos"
               

    def __str__(self):
        return (f"{self.nombre_categoria.capitalize()} , {self.nombre_categoria.capitalize()}")
    
class Gastos(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    tipogasto=models.ForeignKey(TiposGastos, on_delete=models.CASCADE)
    categoria=models.ForeignKey(CategoriaGastos, on_delete=models.CASCADE)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    nombre_gasto=models.CharField(max_length=200,blank=False)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Gastos"
               

    # def __str__(self):
    #     return (f"{self.nombre_gasto.capitalize()} , {self.nombre_gasto.capitalize()}")
        
    def retorno_tipo_gasto_id(self):
        return self.tipogasto_id
    
    def retorno_categoria_gasto_id(self):
        return self.categoria_id
    
    
        
class Egresos(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    gasto=models.ForeignKey(Gastos, on_delete=models.CASCADE)
    monto_gasto=models.IntegerField()
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    fecha_gasto=models.DateField("fecha egresos")
    anotacion=models.CharField(max_length=200,blank=True)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Egresos"
               
    def retorno_gasto_id(self):
        return self.gasto_id

class TiposProductosFinancieros(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    nombre_tipo_producto=models.CharField(max_length=200,blank=False,unique=True)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="TiposProductosFinancieros"
               

    def __str__(self):
        return (f"{self.nombre_tipo_producto.capitalize()} , {self.nombre_tipo_producto.capitalize()}")


class ProductosFinancieros(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    tipoproducto=models.ForeignKey(TiposProductosFinancieros, on_delete=models.CASCADE)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    nombre_producto=models.CharField(max_length=200,blank=False)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="ProductosFinancieros"
                   
    def retorno_tipo_producto_id(self):
        return self.tipoproducto_id
    


class Ingresos(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    producto_financiero=models.ForeignKey(ProductosFinancieros, on_delete=models.CASCADE)
    monto_ingreso=models.IntegerField()
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    fecha_ingreso=models.DateField("fecha ingresos")
    anotacion=models.CharField(max_length=200,blank=True)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Ingresos"
               
    def retorno_producto_financiero_id(self):
        return self.producto_financiero_id
    
    

class SesionesActivas(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    user_name=models.CharField(max_length=100,blank=False)
    fecha_conexion=models.DateTimeField("fecha ultma conexion")
    token_session=models.CharField(max_length=100,blank=True)
    dispositivo=models.CharField(max_length=200,blank=True)
    
    class Meta:
        db_table="SesionesActivas"

    def __str__(self):
        return (f"{self.user_name.capitalize()} , {self.user_name.capitalize()}")
    

class Meses(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    numero_mes=models.IntegerField( default=1)
    nombre_mes=models.CharField(max_length=100,blank=False)
    fecha_registro=models.DateTimeField("fecha_registro")
    
    class Meta:
        db_table="Meses"

    def __str__(self):
        return (f"{self.nombre_mes.capitalize()} , {self.nombre_mes.capitalize()}")


class SolicitudPassword(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    codigo_recuperacion=models.IntegerField()
    fecha_creacion=models.DateTimeField("fecha creacion",blank=False)
    fecha_vencimiento=models.DateTimeField("fecha vencimiento",blank=False)
    fecha_procesamiento=models.DateTimeField("fecha vencimiento",blank=True,null=True)

    class Meta:
        db_table="SolicitudPassword"
                   
    

