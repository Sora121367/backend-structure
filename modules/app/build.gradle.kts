// The bootable application: wires all modules, owns Flyway migrations and application.yml.
plugins {
    id("org.springframework.boot")
}

dependencies {
    implementation(project(":modules:common"))
    implementation(project(":modules:identity-admin"))
    implementation(project(":modules:profile"))
    implementation(project(":modules:classroom"))
    implementation(project(":modules:workspace"))
    implementation(project(":modules:learning-resource"))
    implementation(project(":modules:notification"))

    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-flyway")
    implementation("org.flywaydb:flyway-database-postgresql")
    runtimeOnly("org.postgresql:postgresql")
}
