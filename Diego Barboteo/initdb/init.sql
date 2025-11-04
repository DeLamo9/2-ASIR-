CREATE TABLE impuestos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    numero_impuesto VARCHAR(20) NOT NULL,
    cif_empresa VARCHAR(20) NOT NULL,
    nif_cliente VARCHAR(20) NOT NULL,
    total_a_recaudar FLOAT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    datos LONGTEXT NOT NULL
);