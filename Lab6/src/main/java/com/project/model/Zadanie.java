package com.project.model;

import java.time.LocalDateTime;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
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
@EntityListeners(AuditingEntityListener.class)
@Entity
@Table(name = "zadanie")
public class Zadanie {

    @Id
    @GeneratedValue
    @Column(name = "zadanie_id")
    private Integer zadanieId;

    @NotBlank(message = "Pole nazwa nie mo\u017ce by\u0107 puste!")
    @Column(nullable = false, length = 50)
    private String nazwa;

    @Column(length = 1000)
    private String opis;

    private Integer kolejnosc;

    @CreatedDate
    @Column(name = "dataczas_dodania", nullable = false, updatable = false)
    private LocalDateTime dataczasDodania;

    @NotNull
    @ManyToOne
    @JoinColumn(name = "projekt_id")
    private Projekt projekt;

    public Integer getProjektId() {
        return projekt != null ? projekt.getProjektId() : null;
    }

    public void setProjektId(Integer projektId) {
        if (projekt == null) {
            projekt = new Projekt();
        }
        projekt.setProjektId(projektId);
    }
}
