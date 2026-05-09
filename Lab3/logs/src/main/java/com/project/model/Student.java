package com.project.model;

import java.util.Set;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Index;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "student",
        indexes = { @Index(name = "idx_nazwisko", columnList = "nazwisko", unique = false),
                    @Index(name = "idx_nr_indeksu", columnList = "nr_indeksu", unique = true) })
public class Student {
    
    @Id
    @GeneratedValue
    @Column(name="student_id")
    private Integer studentId;

    @NotBlank
    @Size(min=2, max=50)
    @Column(nullable = false, length = 50)
    private String imie;

    @NotBlank
    @Size(min=2, max=100)
    @Column(nullable = false, length = 100)
    private String nazwisko;

    @NotBlank
    @Size(min=3, max=20)
    @Column(name="nr_indeksu", nullable = false, length = 20, unique = true)
    private String nrIndeksu;

    private Boolean stacjonarny;

    @ManyToMany(mappedBy = "studenci")
    @JsonIgnoreProperties({"studenci"})
    private Set<Projekt> projekty;
}
