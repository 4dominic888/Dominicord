# Bot de discord basado en el usuario 4dominic888.

## Setup

Será necesario crear un archivo `.env` con las siguientes variables:

```env
DISCORD_TOKEN=your-discord-app-token
CLIENT_ID=your-discord-app-client-id
PREFIX=some-prefix
```

Estas se consiguen en el panel administrativo de discord. Recuerda que DISCORD_TOKEN es el token de la aplicación y no CLIENT_SECRET.

Los permisos por defecto son:

- Add reactions
- Attach files
- Connect
- Create Expressions
- Embed links
- Read Message History
- Send Messages
- Speak
- Use voice activity

## Modulos

### Music

Para habilitar este módulo, es necesario crear una carpeta `shared/music` y agregar algunas canciones en formato mp3.
Cabe aclarar que se necesita tener algunas carpetas con algún nombre, estas serviran como playlists.

Finalmente ejecuta esto
```bash
pip install -r requirements.txt
```