package com.project.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import com.project.datasource.DataSource;
import com.project.model.Zadanie;

public class ZadanieDAOImpl implements ZadanieDAO {

    @Override
    public Zadanie getZadanie(Integer zadanieId) {
        try (Connection c = DataSource.getConnection();
             PreparedStatement ps = c.prepareStatement("SELECT * FROM zadanie WHERE zadanie_id=?")) {

            ps.setInt(1, zadanieId);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                Zadanie z = new Zadanie();
                z.setZadanieId(rs.getInt("zadanie_id"));
                z.setNazwa(rs.getString("nazwa"));
                z.setOpis(rs.getString("opis"));
                z.setKolejnosc(rs.getObject("kolejnosc", Integer.class));
                z.setDataCzasUtworzenia(rs.getObject("dataczas_utworzenia", LocalDateTime.class));
                z.setProjektId(rs.getInt("projekt_id"));
                return z;
            }

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return null;
    }

    @Override
    public void setZadanie(Zadanie zadanie) {
        boolean insert = zadanie.getZadanieId() == null;

        String query = insert ?
            "INSERT INTO zadanie(nazwa, opis, kolejnosc, dataczas_utworzenia, projekt_id) VALUES (?, ?, ?, ?, ?)" :
            "UPDATE zadanie SET nazwa = ?, opis = ?, kolejnosc = ?, dataczas_utworzenia = ?, projekt_id = ? WHERE zadanie_id = ?";

        try (Connection connect = DataSource.getConnection();
             PreparedStatement ps = connect.prepareStatement(query, Statement.RETURN_GENERATED_KEYS)) {

            ps.setString(1, zadanie.getNazwa());
            ps.setString(2, zadanie.getOpis());
            ps.setObject(3, zadanie.getKolejnosc());

            if (zadanie.getDataCzasUtworzenia() == null) {
                zadanie.setDataCzasUtworzenia(LocalDateTime.now());
            }
            ps.setObject(4, zadanie.getDataCzasUtworzenia());
            ps.setInt(5, zadanie.getProjektId());

            if (!insert) {
                ps.setInt(6, zadanie.getZadanieId());
            }

            int affectedRows = ps.executeUpdate();

            if (insert && affectedRows > 0) {
                try (ResultSet keys = ps.getGeneratedKeys()) {
                    if (keys.next()) {
                        zadanie.setZadanieId(keys.getInt(1));
                    }
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void deleteZadanie(Integer zadanieId) {
        try (Connection c = DataSource.getConnection();
             PreparedStatement ps = c.prepareStatement("DELETE FROM zadanie WHERE zadanie_id=?")) {

            ps.setInt(1, zadanieId);
            ps.executeUpdate();

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public List<Zadanie> getZadania(Integer projektId) {
        List<Zadanie> list = new ArrayList<>();

        try (Connection c = DataSource.getConnection();
             PreparedStatement ps = c.prepareStatement(
                 "SELECT * FROM zadanie WHERE projekt_id = ? ORDER BY kolejnosc ASC, dataczas_utworzenia ASC")) {

            ps.setInt(1, projektId);
            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
                Zadanie z = new Zadanie();
                z.setZadanieId(rs.getInt("zadanie_id"));
                z.setNazwa(rs.getString("nazwa"));
                z.setOpis(rs.getString("opis"));
                z.setKolejnosc(rs.getObject("kolejnosc", Integer.class));
                z.setDataCzasUtworzenia(rs.getObject("dataczas_utworzenia", LocalDateTime.class));
                z.setProjektId(rs.getInt("projekt_id"));
                list.add(z);
            }

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return list;
    }
}
