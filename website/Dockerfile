# Utiliser une image de base légère comme Nginx
FROM nginx:latest

# Copier les fichiers de votre site web dans le répertoire par défaut de Nginx
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY logo.png /usr/share/nginx/html/

# Exposer le port 80 pour accéder au site web
EXPOSE 80

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]

