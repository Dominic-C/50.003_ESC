package com.example.javatest;

import org.junit.After;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertNotNull;

public class RobustnessTesting {

//  In this class, we test the following:
// - Brute-force login (with 6 attempts), wait for 3 minutes lockout period, before logging in with correct details
// X Redirects when nobody is logged in
// X Redirects when Professor is logged in
// X Redirects when Timetable planner is logged in
// X Redirects when Student is logged in
// X Redirects when Course Coordinator is logged in




    static WebDriver driver;

    final String PASSWORD = "sutd1234";
    final String StudentUserName = "student";
    final String BRUTEPASSWORD = "1111111111";

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
    public void test_login_brute_force() throws InterruptedException {
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

        WebElement username = null;
        WebElement password = null;
        WebElement LoginButton = null;

        // brute-force for 6 times
        for (int i = 0; i < 6; i++) {
            username = driver.findElement(By.id("id_username"));
            username.clear();
            username.sendKeys(StudentUserName);

            password = driver.findElement(By.id("id_password"));
            password.clear();
            password.sendKeys(BRUTEPASSWORD);

            LoginButton = driver.findElement(By.id("id_login"));
            LoginButton.click();

            // checks that we are still in the same page
            String actualURL = driver.getCurrentUrl();
            assertNotNull(actualURL);
            assertEquals("http://127.0.0.1:8000/accounts/login/", actualURL);

        }

        // key in the correct username & password
        username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(StudentUserName);

        password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks that we are still in the same page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/accounts/login/", actualURL);

        // wait for lockout period
//        Thread.sleep(3*60*1000);
        int remainingTime = 3*60;
        while (remainingTime > 0){
            remainingTime --;
            Thread.sleep(1000);
            System.out.println("Remaining seconds: " + remainingTime);
        }

        // key in the correct username & password
        username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(StudentUserName);

        password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks that we are finally logged in
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/students/", actualURL);

    }


}

