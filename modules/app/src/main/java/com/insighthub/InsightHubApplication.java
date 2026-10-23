package com.insighthub;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point of the InsightHub backend.
 *
 * <p>Lives in the root package {@code com.insighthub} on purpose: component scanning, JPA entity
 * scanning and Spring Data repository scanning then cover every module
 * ({@code com.insighthub.classroom}, {@code com.insighthub.workspace}, ...). Don't move it into a
 * sub-package. No business logic here.
 */
@SpringBootApplication
public class InsightHubApplication {

    public static void main(String[] args) {
        SpringApplication.run(InsightHubApplication.class, args);
    }
}