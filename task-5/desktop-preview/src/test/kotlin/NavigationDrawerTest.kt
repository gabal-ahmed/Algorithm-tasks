import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.requiredSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import androidx.compose.ui.graphics.toAwtImage
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import com.example.drawer.ui.NavigationDrawerExample
import org.junit.Rule
import org.junit.Test
import java.io.File
import javax.imageio.ImageIO

class NavigationDrawerTest {
    @get:Rule
    val rule = createComposeRule()

    private fun shot(name: String) {
        val dir = File(System.getProperty("screenshots.dir")).apply { mkdirs() }
        val img = rule.onNodeWithTag("phone").captureToImage().toAwtImage()
        ImageIO.write(img, "png", File(dir, "$name.png"))
    }

    @Test
    fun drawerFlow() {
        rule.mainClock.autoAdvance = true
        // Phone-sized frame (412 x 740 dp) so screenshots look like a device screen
        rule.setContent {
            Box(Modifier.requiredSize(412.dp, 740.dp).testTag("phone")) {
                MaterialTheme { NavigationDrawerExample() }
            }
        }

        // 1) Start: drawer closed, Home selected
        rule.onNodeWithText("Showing: Home").assertIsDisplayed()
        shot("1-home-closed")

        // 2) Tap the menu icon -> drawer opens
        rule.onNodeWithContentDescription("Menu").performClick()
        rule.waitForIdle()
        rule.onNodeWithText("Profile").assertIsDisplayed()
        shot("2-drawer-open")

        // 3) Pick "Profile" -> drawer closes, title and body update
        rule.onNodeWithText("Profile").performClick()
        rule.waitForIdle()
        rule.onNodeWithText("Showing: Profile").assertIsDisplayed()
        shot("3-profile-selected")

        // 4) Open again and pick "Settings"
        rule.onNodeWithContentDescription("Menu").performClick()
        rule.waitForIdle()
        rule.onNodeWithText("Settings").performClick()
        rule.waitForIdle()
        rule.onNodeWithText("Showing: Settings").assertIsDisplayed()
        shot("4-settings-selected")
    }
}
