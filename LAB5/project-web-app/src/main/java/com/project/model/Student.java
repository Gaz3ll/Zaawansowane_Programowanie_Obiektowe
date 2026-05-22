package com.project.model;

import java.util.Set;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class Student {

    private Integer studentId;

    @NotBlank(message = "Pole imię nie może być puste!")
    @Size(min = 2, max = 50, message = "Imię musi zawierać od {min} do {max} znaków!")
    private String imie;

    @NotBlank(message = "Pole nazwisko nie może być puste!")
    @Size(min = 2, max = 100, message = "Nazwisko musi zawierać od {min} do {max} znaków!")
    private String nazwisko;

    @NotBlank(message = "Pole nr indeksu nie może być puste!")
    @Size(min = 3, max = 20, message = "Nr indeksu musi zawierać od {min} do {max} znaków!")
    private String nrIndeksu;

    private Boolean stacjonarny;

    @JsonIgnoreProperties({ "studenci", "zadania" })
    private Set<Projekt> projekty;
}
