FROM nginx:alpine

# Remove default nginx static html files
RUN rm -rf /usr/share/nginx/html/*

# Copy custom frontend static web assets
COPY index.html /usr/share/nginx/html/index.html

# Copy custom reverse proxy nginx server configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Built-in alpine healthcheck using wget
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]