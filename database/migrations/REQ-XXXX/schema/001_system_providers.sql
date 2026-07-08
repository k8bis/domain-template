CREATE TABLE system_providers (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    provider_code VARCHAR(100) NOT NULL,
    provider_name VARCHAR(150) NOT NULL,
    description TEXT NULL,

    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT uq_system_providers_code
        UNIQUE (provider_code)
);