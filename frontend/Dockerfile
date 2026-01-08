# ---------- Build Stage ----------
FROM node:20-alpine AS build

WORKDIR /app

# Package-Dateien kopieren und Dependencies installieren
COPY package.json package-lock.json ./
RUN npm install

# Quellcode kopieren und bauen
COPY . .
RUN npm run build

# ---------- Runtime Stage ----------
FROM nginx:alpine

# Standard-Nginx-Konfiguration entfernen
RUN rm /etc/nginx/conf.d/default.conf

# Eigene Nginx-Konfiguration kopieren
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Gebautes Frontend kopieren
COPY --from=build /app/dist /usr/share/nginx/html

# Port freigeben
EXPOSE 80

# Nginx starten
CMD ["nginx", "-g", "daemon off;"]
