# 🚀 Guía de Despliegue - Water Delivery System

## 📋 Requisitos Previos

- Python 3.11+
- Git
- Cuenta en Railway/Render/DigitalOcean

## 🎯 Opciones de Hosting Recomendadas

### 1. Railway (Recomendado - Más Económico)
- **Precio**: $5-20/mes
- **Ventajas**: Despliegue automático, base de datos incluida, SSL gratuito
- **URL**: https://railway.app

### 2. Render
- **Precio**: $7/mes
- **Ventajas**: Fácil configuración, SSL gratuito
- **URL**: https://render.com

### 3. DigitalOcean (Para Producción Profesional)
- **Precio**: $6-12/mes
- **Ventajas**: Control total, muy confiable
- **URL**: https://digitalocean.com

## 🚀 Despliegue en Railway (Recomendado)

### Paso 1: Preparar el Repositorio
```bash
# Asegúrate de que todos los archivos estén en GitHub
git add .
git commit -m "Preparar para despliegue"
git push origin main
```

### Paso 2: Crear Proyecto en Railway
1. Ve a https://railway.app
2. Crea una cuenta o inicia sesión
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Conecta tu repositorio de GitHub

### Paso 3: Configurar Variables de Entorno
En Railway, ve a la pestaña "Variables" y agrega:

```env
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=False
ALLOWED_HOSTS=tu-app.railway.app
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
```

### Paso 4: Configurar Base de Datos
1. En Railway, ve a "New Service" → "Database" → "PostgreSQL"
2. Railway automáticamente configurará `DATABASE_URL`
3. Copia la URL de la base de datos a las variables de entorno

### Paso 5: Desplegar
1. Railway detectará automáticamente que es un proyecto Django
2. El despliegue comenzará automáticamente
3. Ve a la pestaña "Deployments" para ver el progreso

## 🔧 Configuración Post-Despliegue

### Crear Superusuario
```bash
# En Railway, ve a la pestaña "Deployments" → "View Logs"
# Ejecuta:
python manage.py createsuperuser
```

### Ejecutar Migraciones
```bash
# Railway ejecuta esto automáticamente, pero puedes verificarlo
python manage.py migrate
```

## 🔄 Actualizaciones Futuras

### Método 1: Despliegue Automático (Recomendado)
1. Haz cambios en tu código local
2. Sube a GitHub: `git push origin main`
3. Railway detectará los cambios y desplegará automáticamente

### Método 2: Despliegue Manual
1. En Railway, ve a "Deployments"
2. Haz clic en "Deploy Now"

## 📊 Monitoreo y Mantenimiento

### Ver Logs
- En Railway: Pestaña "Deployments" → "View Logs"
- Útil para debugging

### Variables de Entorno
- En Railway: Pestaña "Variables"
- Aquí puedes cambiar configuraciones sin redeploy

### Base de Datos
- En Railway: Pestaña "Connect" → "Connect to Database"
- Para hacer backups o consultas directas

## 🔒 Seguridad en Producción

### Variables de Entorno Obligatorias
```env
SECRET_KEY=clave-muy-segura-y-única
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
```

### Configuraciones de Seguridad
- SSL automático en Railway
- Headers de seguridad configurados
- CSRF protection activado

## 💰 Costos Estimados

### Railway
- **Plan Básico**: $5/mes (1GB RAM, 1 CPU)
- **Plan Estándar**: $20/mes (2GB RAM, 2 CPU)
- **Base de datos**: Incluida en el plan

### Render
- **Plan Básico**: $7/mes
- **Base de datos**: $7/mes adicional

### DigitalOcean
- **Droplet Básico**: $6/mes
- **Base de datos**: $15/mes adicional

## 🆘 Solución de Problemas

### Error: "No module named 'decouple'"
```bash
# Agregar a requirements.txt:
python-decouple==3.8
```

### Error: "Static files not found"
```bash
# Verificar que whitenoise esté en MIDDLEWARE
# Ejecutar: python manage.py collectstatic
```

### Error: "Database connection failed"
- Verificar `DATABASE_URL` en variables de entorno
- Asegurar que la base de datos esté activa

## 📞 Soporte

### Para el Cliente
- Proporcionar acceso al panel de Railway
- Documentar credenciales de administrador
- Crear guía de usuario básica

### Para el Desarrollador
- Mantener acceso al repositorio GitHub
- Configurar notificaciones de despliegue
- Documentar cambios importantes

## 🎯 Próximos Pasos

1. **Desplegar en Railway** (más económico)
2. **Configurar dominio personalizado** (opcional)
3. **Configurar email** para notificaciones
4. **Crear backup automático** de la base de datos
5. **Configurar monitoreo** de la aplicación

---

**¡Tu proyecto está listo para producción! 🚀** 