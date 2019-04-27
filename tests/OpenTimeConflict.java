package com.example.dominic.esc_selenium;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;

public class OpenTimeConflict {

    public static void main(String[] args) {

        // set the firefox driver
        System.setProperty("webdriver.gecko.driver","/home/dominic/Documents/school/ESC/geckodriver");
        //System.setProperty("webdriver.chrome.driver","/Users/sudiptac/sudiptac/teaching/SUTD/50.003@2018/Test/chromedriver");
        WebDriver driver = new FirefoxDriver();
        //WebDriver driver = new ChromeDriver();

        // open my webpage
        driver.get("http://127.0.0.1:8000/schedule/testingdropdown");

        // click the link with name "press release"
//        driver.findElement(By.linkText("ASSET Research Group")).click();
        WebElement title = driver.findElement(By.name("title"));
        title.sendKeys("50.003 ESC");

        Select start = new Select(driver.findElement(By.name("start_time")));
        start.selectByIndex(1);

        Select end = new Select(driver.findElement(By.name("end_time")));
        end.selectByIndex(10);

        Select lecturer = new Select(driver.findElement(By.name("lecturer")));
        lecturer.selectByIndex(2);

        Select location = new Select(driver.findElement(By.name("location")));
        location.selectByIndex(1);

        WebElement submit = driver.findElement(By.name("submit"));
        submit.click();

        // second overlapping entry
        title.sendKeys("50.003 ESC");
        start.selectByIndex(1);
        end.selectByIndex(10);
        lecturer.selectByIndex(2);
        location.selectByIndex(1);
        submit.click();


        // click the link name "Event"
//        driver.findElement(By.linkText("Sakshi Udeshi")).click();

        // click the link name "Newsletter"
//        driver.findElement(By.linkText("facebook")).click();

    }
}
