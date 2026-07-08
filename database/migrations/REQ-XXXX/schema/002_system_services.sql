CREATE TABLE system_services (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    provider_id BIGINT NOT NULL,

    service_code VARCHAR(100) NOT NULL,
    service_name VARCHAR(150) NOT NULL,
    description TEXT NULL,

    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_system_services_provider
        FOREIGN KEY (provider_id)
        REFERENCES system_providers(id),

    CONSTRAINT uq_system_services_provider_code
        UNIQUE (provider_id, service_code)
);