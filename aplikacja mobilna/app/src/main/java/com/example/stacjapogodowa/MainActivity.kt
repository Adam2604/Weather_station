package com.example.stacjapogodowa

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.stacjapogodowa.ui.theme.StacjaPogodowaTheme
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val webView: WebView = findViewById(R.id.webview)

        // włączenie obsługi JavaScript (jeśli strona go potrzebuje)
        webView.settings.javaScriptEnabled = true

        // żeby linki otwierały się w aplikacji, a nie w przeglądarce
        webView.webViewClient = WebViewClient()

        // tutaj wpisujesz adres swojej strony Flask
        webView.loadUrl("http://192.168.34.15:5000")
    }
}


@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    StacjaPogodowaTheme {
        Greeting("Android")
    }
}