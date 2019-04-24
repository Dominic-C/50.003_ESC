package com.example.javatest;

import org.junit.After;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

import java.util.concurrent.TimeUnit;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertNotNull;

public class IntegrationTests {

    static WebDriver driver;
    final String ProfUserName = "professor";
    final String PlannerUserName = "planner";
    final String PASSWORD = "sutd1234";


    @BeforeClass
    public static void setup() {
        System.setProperty("webdriver.gecko.driver", "C:\\Users\\It'sMine\\AndroidStudioProjects\\JavaTest\\Javatest\\libs\\geckodriver.exe");
        driver = new FirefoxDriver();
    }

    @After
    public void logout() {
        driver.get("http://127.0.0.1:8000");
        java.util.List<WebElement> links = driver.findElements(By.tagName("a"));

        // find Log out button
        WebElement logoutButton = null;
        for (WebElement link : links) {
            if (link.getText().equals("Log out")) {
                logoutButton = link;
            }
        }
        if (logoutButton != null) logoutButton.click();
    }

    @Test
    public void test_planner_calendar(){
        driver.get("http://127.0.0.1:8000");
        java.util.List<WebElement> links = driver.findElements(By.tagName("a"));

        // find Log in button
        WebElement loginButton = null;
        for (WebElement link : links) {
            if (link.getText().equals("Log in")) {
                loginButton = link;
            }
        }

        if (loginButton != null) {
            loginButton.click();
        }

        WebElement username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(PlannerUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/", actualURL);

        // clicks dropdown and goes to Upload First Draft
        java.util.List<WebElement> dropdowns = driver.findElements(By.id("navbarDropdown"));
        WebElement dropdown = null;
        for (WebElement item: dropdowns){
            if (item.getText().equals("Finalisation")){
                dropdown = item;
                break;
            }
        }
        dropdown.click();

        java.util.List<WebElement> dropdownItems = driver.findElements(By.className("dropdown-item"));
        WebElement viewCalendar = null;
        for (WebElement item : dropdownItems) {
            if (item.getText().equals("View Calendar")) {
                viewCalendar = item;
                break;
            }
        }

        if (viewCalendar != null) viewCalendar.click();

        // checks if we are in view calendar page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/schedule/", actualURL);
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement calendar = driver.findElement(By.className("ds-calendar"));
        assertNotNull(calendar);

    }
}
