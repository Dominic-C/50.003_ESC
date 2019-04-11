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
import static junit.framework.TestCase.assertTrue;

public class RobustnessTesting {

//  In this class, we test the following:
// - Brute-force login (with 6 attempts), wait for 3 minutes lockout period, before logging in with correct details
// - Redirects when nobody is logged in
// - Redirects when Professor is logged in
// - Redirects when Timetable planner is logged in
// - Redirects when Student is logged in
// - Redirects when Course Coordinator is logged in




    static WebDriver driver;

    final String ProfUserName = "professor";
    final String PlannerUserName = "planner";
    final String StudentUserName = "student";
    final String CoordinatorUserName = "coordinator";

    final String PASSWORD = "sutd1234";
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
    public void test_redirects_nobody_logged_in(){
        driver.get("http://127.0.0.1:8000/professors");
        // checks that we are redirected
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/submitdetails");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/students");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/coordinators");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/sutdadmin");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/export");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/upload");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/phase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/nextphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/prevphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/downloadsample");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));
    }

    @Test
    public void test_redirects_student_logged_in(){
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
        username.sendKeys(StudentUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/students/", actualURL);

        driver.get("http://127.0.0.1:8000/professors");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/submitdetails");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/coordinators");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/sutdadmin");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/export");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/upload");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/phase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/nextphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/prevphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/downloadsample");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));
    }

    @Test
    public void test_redirects_coordinator_logged_in() {
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
        username.sendKeys(CoordinatorUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/coordinators/", actualURL);

        driver.get("http://127.0.0.1:8000/professors");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/submitdetails");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/students");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/sutdadmin");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/export");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/upload");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/phase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/nextphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/prevphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/downloadsample");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));


    }


    @Test
    public void test_redirects_prof_logged_in(){
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
        username.sendKeys(ProfUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/professors/", actualURL);

        driver.get("http://127.0.0.1:8000/professors");
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/professors"));

        driver.get("http://127.0.0.1:8000/professors/submitdetails");
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/professors/submitdetails"));

        driver.get("http://127.0.0.1:8000/professors/details");
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/professors/details"));

        driver.get("http://127.0.0.1:8000/students");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/coordinators");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/sutdadmin");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/export");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/upload");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/phase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/nextphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/prevphase");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners/downloadsample");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

    }

    @Test
    public void test_redirects_planner_logged_in() {
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

        driver.get("http://127.0.0.1:8000/professors");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/submitdetails");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/professors/details");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/students");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/coordinators");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/sutdadmin");
        // checks that we are redirected
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/accounts/login/"));

        driver.get("http://127.0.0.1:8000/planners");
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/planners"));

        driver.get("http://127.0.0.1:8000/planners/upload");
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/planners/upload"));

        driver.get("http://127.0.0.1:8000/planners/phase");
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertTrue(actualURL.startsWith("http://127.0.0.1:8000/planners/phase"));

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

