async function runTest() {
      console.log("🚀 Starting JS Load Test...\n");

      const urls = [
            "http://127.0.0.1:8000/",
            "http://127.0.0.1:8000/articles/",
            "http://127.0.0.1:8000/accounts/login/",
            "http://127.0.0.1:8000/analysis/"
      ];

      const requests = 1000;
      let total = 0;
      let success = 0;
      let fail = 0;

      const startTest = Date.now();

      for (let i = 0; i < requests; i++) {

            const url = urls[i % urls.length]; // rotate endpoints
            const start = Date.now();

            try {
                  const res = await fetch(url);
                  await res.text();

                  const end = Date.now();
                  const time = end - start;

                  total += time;
                  success++;

                  console.log(`Request ${i + 1} → ${url} : ${time} ms`);

            } catch (err) {
                  fail++;
                  console.log(`Request ${i + 1}: ERROR`);
            }
      }

      const endTest = Date.now();
      const totalTimeSec = (endTest - startTest) / 1000;

      const avgTime = total / requests;
      const rps = requests / totalTimeSec;

      console.log("\n========== RESULT ==========");
      console.log("Total Requests:", requests);
      console.log("Success:", success);
      console.log("Failed:", fail);
      console.log("Average Time:", avgTime.toFixed(2), "ms");
      console.log("Total Time:", totalTimeSec.toFixed(2), "sec");
      console.log("🔥 Requests Per Second (RPS):", rps.toFixed(2));
      console.log("================================");
}

runTest();