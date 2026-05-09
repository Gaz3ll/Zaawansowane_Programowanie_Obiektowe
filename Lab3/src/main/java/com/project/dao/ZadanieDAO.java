package com.project.dao;

import java.util.List;
import com.project.model.Zadanie;

public interface ZadanieDAO {
    Zadanie getZadanie(Integer zadanieId);
    void setZadanie(Zadanie zadanie);
    void deleteZadanie(Integer zadanieId);
    List<Zadanie> getZadania(Integer projektId);
}
