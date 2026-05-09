package com.project.dao;

import java.sql.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

import com.project.datasource.DataSource;
import com.project.model.Projekt;

public class ProjektDAOImpl implements ProjektDAO {

   @Override
   public void setProjekt(Projekt p) {
      boolean insert = p.getProjektId() == null;

      String sql = insert ?
         "INSERT INTO projekt(nazwa,opis,dataczas_utworzenia,data_oddania) VALUES(?,?,?,?)"
         :
         "UPDATE projekt SET nazwa=?,opis=?,dataczas_utworzenia=?,data_oddania=? WHERE projekt_id=?";

      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {

         ps.setString(1, p.getNazwa());
         ps.setString(2, p.getOpis());

         if (p.getDataCzasUtworzenia() == null)
            p.setDataCzasUtworzenia(LocalDateTime.now());

         ps.setObject(3, p.getDataCzasUtworzenia());
         ps.setObject(4, p.getDataOddania());

         if (!insert) ps.setInt(5, p.getProjektId());

         ps.executeUpdate();

         if (insert) {
            ResultSet rs = ps.getGeneratedKeys();
            if (rs.next()) p.setProjektId(rs.getInt(1));
         }

      } catch (Exception e) {
         throw new RuntimeException(e);
      }
   }

   @Override
   public Projekt getProjekt(Integer id) {
      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement("SELECT * FROM projekt WHERE projekt_id=?")) {

         ps.setInt(1, id);
         ResultSet rs = ps.executeQuery();

         if (rs.next()) {
            Projekt p = new Projekt();
            p.setProjektId(rs.getInt(1));
            p.setNazwa(rs.getString(2));
            p.setOpis(rs.getString(3));
            p.setDataCzasUtworzenia(rs.getObject(4, LocalDateTime.class));
            p.setDataOddania(rs.getObject(5, LocalDate.class));
            return p;
         }

      } catch (Exception e) {
         throw new RuntimeException(e);
      }
      return null;
   }

   @Override
   public void deleteProjekt(Integer id) {
      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement("DELETE FROM projekt WHERE projekt_id=?")) {

         ps.setInt(1, id);
         ps.executeUpdate();

      } catch (Exception e) {
         throw new RuntimeException(e);
      }
   }

   @Override
   public List<Projekt> getProjekty(Integer offset, Integer limit) {
      List<Projekt> list = new ArrayList<>();

      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement(
               "SELECT * FROM projekt ORDER BY dataczas_utworzenia DESC LIMIT ? OFFSET ?")) {

         ps.setInt(1, limit);
         ps.setInt(2, offset);

         ResultSet rs = ps.executeQuery();

         while (rs.next()) {
            Projekt p = new Projekt();
            p.setProjektId(rs.getInt(1));
            p.setNazwa(rs.getString(2));
            p.setOpis(rs.getString(3));
            p.setDataCzasUtworzenia(rs.getObject(4, LocalDateTime.class));
            p.setDataOddania(rs.getObject(5, LocalDate.class));
            list.add(p);
         }

      } catch (Exception e) {
         throw new RuntimeException(e);
      }
      return list;
   }

   @Override
   public List<Projekt> getProjektyWhereNazwaLike(String nazwa, Integer offset, Integer limit) {
      List<Projekt> list = new ArrayList<>();
      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement(
               "SELECT * FROM projekt WHERE nazwa LIKE ? ORDER BY dataczas_utworzenia DESC LIMIT ? OFFSET ?")) {
         ps.setString(1, "%" + nazwa + "%");
         ps.setInt(2, limit);
         ps.setInt(3, offset);
         ResultSet rs = ps.executeQuery();
         while (rs.next()) {
            Projekt p = new Projekt();
            p.setProjektId(rs.getInt(1));
            p.setNazwa(rs.getString(2));
            p.setOpis(rs.getString(3));
            p.setDataCzasUtworzenia(rs.getObject(4, LocalDateTime.class));
            p.setDataOddania(rs.getObject(5, LocalDate.class));
            list.add(p);
         }
      } catch (Exception e) {
         throw new RuntimeException(e);
      }
      return list;
   }

   @Override
   public List<Projekt> getProjektyWhereDataOddaniaIs(LocalDate data, Integer offset, Integer limit) {
      List<Projekt> list = new ArrayList<>();
      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement(
               "SELECT * FROM projekt WHERE data_oddania = ? ORDER BY dataczas_utworzenia DESC LIMIT ? OFFSET ?")) {
         ps.setObject(1, data);
         ps.setInt(2, limit);
         ps.setInt(3, offset);
         ResultSet rs = ps.executeQuery();
         while (rs.next()) {
            Projekt p = new Projekt();
            p.setProjektId(rs.getInt(1));
            p.setNazwa(rs.getString(2));
            p.setOpis(rs.getString(3));
            p.setDataCzasUtworzenia(rs.getObject(4, LocalDateTime.class));
            p.setDataOddania(rs.getObject(5, LocalDate.class));
            list.add(p);
         }
      } catch (Exception e) {
         throw new RuntimeException(e);
      }
      return list;
   }

   @Override
   public int getRowsNumber() {
      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement("SELECT COUNT(*) FROM projekt")) {
         ResultSet rs = ps.executeQuery();
         if (rs.next()) return rs.getInt(1);
      } catch (Exception e) {
         throw new RuntimeException(e);
      }
      return 0;
   }

   @Override
   public int getRowsNumberWhereNazwaLike(String nazwa) {
      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement("SELECT COUNT(*) FROM projekt WHERE nazwa LIKE ?")) {
         ps.setString(1, "%" + nazwa + "%");
         ResultSet rs = ps.executeQuery();
         if (rs.next()) return rs.getInt(1);
      } catch (Exception e) {
         throw new RuntimeException(e);
      }
      return 0;
   }

   @Override
   public int getRowsNumberWhereDataOddaniaIs(LocalDate dataOddania) {
      try (Connection c = DataSource.getConnection();
           PreparedStatement ps = c.prepareStatement("SELECT COUNT(*) FROM projekt WHERE data_oddania = ?")) {
         ps.setObject(1, dataOddania);
         ResultSet rs = ps.executeQuery();
         if (rs.next()) return rs.getInt(1);
      } catch (Exception e) {
         throw new RuntimeException(e);
      }
      return 0;
   }
}