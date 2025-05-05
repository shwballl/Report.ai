import React from "react";

export default function LandingPage() {
    const [selectedOption, setSelectedOption] = React.useState("");
    const [url, setURL] = React.useState("");
    const [reportHTML, setReportHTML] = React.useState("");

    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState("");

    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
    };

    const handleURLChange = (event) => {
        setURL(event.target.value);
    };

    const handleGetReport = async () => {
        setLoading(true);
        setError("");

        try {
            const response = await fetch("http://localhost:8000/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    url,
                    analysis_type: selectedOption || null,
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to generate report");
            }

            const data = await response.json();

            if (data.status === "OK") {
                if (data.report_path) {
                    const reportRes = await fetch("http://localhost:8000/report");
                    const html = await reportRes.text();
                    setReportHTML(html);
                }
            } else {
                throw new Error("Unexpected response");
            }
        } catch (err) {
            console.error(err);
            setError("Failed to analyze the repository.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div className="bg-[#FDFFCE]">
                <div className="text-2xl font-semibold py-2.5 px-4 text-gray-900  bg-[static_url('bg.svg')]">
                    Report<span className="text-orange-500">.ai</span>
                </div>
                <div className="my-30 bg-[#FDFFCE] flex flex-col items-center justify-center relative ">


                    {/* Header */}
                    <div className="text-center mb-8 justify-center">
                        <img src="crown.svg" className="inline-block" alt="" />
                        <img src="text.svg" alt="" />
                    </div>

                    {/* Form */}
                    <div className="w-full max-w-sm space-y-4">
                        <input
                            type="text"
                            placeholder="url"
                            className="w-full px-4 py-2 rounded-lg bg-gray-200 placeholder-gray-600"
                            onChange={handleURLChange}
                        />
                        <input
                            type="text"
                            placeholder="analyze category"
                            className="w-full px-4 py-2 rounded-lg bg-gray-200 placeholder-gray-600"
                            onChange={handleOptionChange}
                        />
                        <button
                            className="w-full bg-black text-white py-2 rounded-lg hover:bg-gray-800 transition hover:cursor-pointer"
                            onClick={handleGetReport}
                            disabled={loading}
                        >
                            {loading ? "Generating..." : "Get report!"}
                        </button>

                        {error && <p className="text-red-600 text-center">{error}</p>}
                    </div>



                    {/* Report Output */}

                </div>

            </div>
            <div className="left-0 w-full bg-[#FDFFCE]">
                {reportHTML && (
                    <div className="bg-[#FDFFCE] max-w-5xl w-6xl mt-16 bg-[#FDFFCE] p-6 left-0">
                        <div
                            className="prose"
                            dangerouslySetInnerHTML={{ __html: reportHTML }}
                        />
                    </div>
                )}
            </div>
        </>
    );
}
