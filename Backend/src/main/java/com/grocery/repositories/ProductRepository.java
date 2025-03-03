package com.grocery.repositories;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import javax.management.RuntimeErrorException;
import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.grocery.models.Product;

@Repository
public class ProductRepository {
    DataSource source;
    @Autowired
    public ProductRepository(DataSource source){this.source = source;}

    public Product getProductByID(String ProductID){
        try{
            Connection connection = this.source.getConnection();
            PreparedStatement stm = connection.prepareStatement("SELECT * FROM Products WHERE ProductID ='"+ProductID+"'");
            ResultSet result = stm.executeQuery();
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
}