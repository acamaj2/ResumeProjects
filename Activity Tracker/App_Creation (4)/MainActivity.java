package com.example.lab5activitytracker; 
 
import androidx.appcompat.app.AppCompatActivity; 
 
import android.os.Bundle; 
import android.os.Handler; 
import android.os.Message; 
import android.view.View; 
import android.widget.CompoundButton; 
import android.widget.Space; 
import android.widget.Switch; 
import android.widget.TableLayout; 
import android.widget.TableRow; 
import android.widget.TextView; 
 
import com.android.volley.Request; 
import com.android.volley.RequestQueue; 
import com.android.volley.Response; 
import com.android.volley.VolleyError; 
import com.android.volley.toolbox.StringRequest; 
import com.android.volley.toolbox.Volley; 
 
import org.json.JSONArray; 
import org.json.JSONException; 
import org.json.JSONObject; 
 
import java.text.DateFormat; 
import java.util.Date; 
import java.util.Timer; 
import java.util.TimerTask; 
 
public class MainActivity extends AppCompatActivity implements CompoundButton.OnCheckedChangeListener, Response.Listener<String>, Response.ErrorListener { 
    private Switch activateLoaderSwitch; 
    private View loadingIndicator; 
    private TableLayout resultsTable; 
 
    private Timer readerTimer; 
    private Handler doLoadDataHandler; 
    private boolean loading; 
 
    private RequestQueue requestQueue; 
 
    @Override 
    protected void onCreate(Bundle savedInstanceState) { 
        super.onCreate(savedInstanceState); 
        setContentView(R.layout.activity_main); 
 
        loadingIndicator = findViewById(R.id.loadingProgress); 
        loadingIndicator.setVisibility(View.INVISIBLE); 
 
        activateLoaderSwitch = findViewById(R.id.activateLoaderSwitch); 
        resultsTable = findViewById(R.id.resultsTable); 
 
        activateLoaderSwitch.setOnCheckedChangeListener(this); 
 
        MainActivity outer = this; 
        doLoadDataHandler = new Handler(this.getMainLooper()) { 
            @Override 
            public void handleMessage(Message msg) { 
                outer.doLoadData(); 
            } 
        }; 
 
        requestQueue = Volley.newRequestQueue(this); 
    } 
 
    @Override 
    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) { 
        if (buttonView == activateLoaderSwitch) { 
            if (isChecked) { 
                readerTimer = new Timer(); 
                readerTimer.scheduleAtFixedRate(new TimerTask() { 
                    @Override 
                    public void run() { 
                        doLoadDataHandler.obtainMessage().sendToTarget(); 
                    } 
                }, 0, 5000); 
            } else { 
                readerTimer.cancel(); 
                readerTimer = null; 
            } 
        } 
    } 
 
    private void doLoadData() { 
        if (this.loading) { 
            return; 
        } 
 
        this.loading = true; 
        loadingIndicator.setVisibility(View.VISIBLE); 
 
        String url = "YOUR_CLOUD_FUNCTION_URL"; 
        this.requestQueue.add(new StringRequest(Request.Method.GET, url, this, this)); 
    } 
 
    @Override 
    public void onResponse(String response) { 
        try { 
            resultsTable.removeAllViews(); 
 
            JSONArray activities = new JSONArray(response); 
 
            JSONObject lastActivity = null; 
            Date activityPeriodStart = null; 
            for (int i = 0; i < activities.length(); i++) { 
                JSONObject activity = activities.getJSONObject(i); 
                System.out.println(activity); 
 
                // Check to see if there was a previous activity 
                if (lastActivity != null) { 
                    // Now, compare the activity types 
                    if (!lastActivity.getString("activity").equalsIgnoreCase(activity.getString("activity"))) { 
                        // If the activity types are different, then terminate the current activity period, 
                        // and start a new one. 
 
                        appendActivityPeriod(activityPeriodStart, new Date(activity.getLong("timestamp")), lastActivity.getString("activity")); 
                        activityPeriodStart = new Date(activity.getLong("timestamp")); 
                    } 
                } else { 
                    // There was no previous activity, so start a new activity period. 
                    activityPeriodStart = new Date(activity.getLong("timestamp")); 
                } 
 
                lastActivity = activity; 
            } 
        } catch (JSONException e) { 
            e.printStackTrace(); 
        } finally { 
            loadingIndicator.setVisibility(View.INVISIBLE); 
            this.loading = false; 
        } 
    } 
 
    @Override 
    public void onErrorResponse(VolleyError error) { 
        System.out.println(error.getMessage()); 
 
        loadingIndicator.setVisibility(View.INVISIBLE); 
        this.loading = false; 
    } 
 
    private void appendActivityPeriod(Date periodStart, Date periodEnd, String activity) { 
        TableRow row = new TableRow(this.getBaseContext()); 
 
        DateFormat fmt = DateFormat.getDateTimeInstance(); 
 
        TextView startTimestamp = new TextView(this.getBaseContext()); 
        startTimestamp.setText(fmt.format(periodStart)); 
        row.addView(startTimestamp); 
 
        Space s = new Space(this.getBaseContext()); 
        s.setMinimumWidth(32); 
        row.addView(s); 
 
        TextView endTimestamp = new TextView(this.getBaseContext()); 
        endTimestamp.setText(fmt.format(periodEnd)); 
        row.addView(endTimestamp); 
 
        Space s2 = new Space(this.getBaseContext()); 
        s2.setMinimumWidth(32); 
        row.addView(s2); 
 
        TextView activityText = new TextView(this.getBaseContext()); 
        activityText.setText(activity); 
        row.addView(activityText); 
 
        resultsTable.addView(row); 
    } 
} 
