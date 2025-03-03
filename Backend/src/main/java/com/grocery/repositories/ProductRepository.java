package com.grocery.repositories;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.LinkedList;
import java.util.List;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.grocery.models.Price;
import com.grocery.models.Product;

@Repository
public class ProductRepository {
    DataSource source;
    @Autowired
    public ProductRepository(DataSource source){this.source = source;}

    public Product getProductByID(String ProductID){
        try{
            Connection connection = this.source.getConnection();
            PreparedStatement stm = connection.prepareStatement("SELECT * FROM Products WHERE ProductID = ?");
            // index starts at 1 :( absolutely devestating
            stm.setString(1, ProductID);
            ResultSet result = stm.executeQuery();
            //Ensure the query yielded a result
            if (result.wasNull()) {
                return null;
            }
            result.next();
            Product product = new Product(result.getString("ProductID"), result.getString("Name"), result.getString("CategoryID"));
            return product;
        }
        catch (SQLException e){
            throw new RuntimeException("Error in findID",e);
        }
    }
    public List<Price> getAllPrices(String ProductID){
        try {
            Connection connection = this.source.getConnection();
            PreparedStatement stm = connection.prepareStatement("SELECT * FROM ProductPrice WHERE ProductID = ?");
            stm.setString(1, ProductID);
            ResultSet result = stm.executeQuery();
            //Ensure the query yielded a result
            if (result.wasNull()) {
                return null;
            }
            List<Price> allPrices = new LinkedList<Price>();
            while (result.next()) {
                Price newprice = new Price(result.getString("ProductID"), result.getString("Price"), result.getString("Date"));
                allPrices.add(newprice);
            }
            return allPrices;
        } catch (Exception e) {
            throw new RuntimeException("Error in getAllPrices",e);
        }
    }

    public Price getCurrentPrice(String ProductID){
        try {
            Connection connection = this.source.getConnection();
            PreparedStatement stm = connection.prepareStatement("SELECT TOP 1 * FROM ProductPrice WHERE ProductID = ? ORDER BY Date DESC");
            stm.setString(1, ProductID);
            ResultSet result = stm.executeQuery();
            //Ensure the query yielded a result
            if (result.wasNull()) {
                return null;
            }
            result.next();
            Price price = new Price(result.getString("ProductID"), result.getString("Price"), result.getString("Date"));
            return price;

        } catch (Exception e) {
            throw new RuntimeException("Error in getCurrentPrice",e);
        }
    }
}