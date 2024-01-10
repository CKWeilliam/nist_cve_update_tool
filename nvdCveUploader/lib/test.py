def get_cve_info(cve_data):
    return [{"id": cve["cve"]["id"],
            "descriptions": {
                desc["lang"]: desc["value"]
                for desc in cve["cve"]["descriptions"]
            },
            "vulnerable": [{"criteria": match["criteria"], 
            "vulnerable": match["vulnerable"]}
                for node in cve["cve"]["configurations"]["nodes"]
                for match in node["cpe_match"]
            ]
        }
        for cve in cve_data
    ]