import os
import json
from datetime import datetime
from config.config import Config

class ReportGenerator:
    def __init__(self):
        self.report_data = {}
    
    def generate_summary_txt(self, test_results, total_time):
        """Generate a simple text summary file"""
        passed_tests = [t for t in test_results if t['status'] == 'PASS']
        failed_tests = [t for t in test_results if t['status'] == 'FAIL']
        
        summary_content = f"""
E-COMMERCE TESTING SUITE - EXECUTION SUMMARY
============================================

Execution Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Duration: {total_time:.2f} seconds

TEST RESULTS SUMMARY:
====================
Total Tests Run: {len(test_results)}
Tests Passed: {len(passed_tests)}
Tests Failed: {len(failed_tests)}
Success Rate: {(len(passed_tests)/len(test_results)*100 if test_results else 0):.1f}%

DETAILED BREAKDOWN BY MODULE:
=============================
"""
        # Group by module
        modules = {}
        for test in test_results:
            module = test['module']
            if module not in modules:
                modules[module] = {'total': 0, 'passed': 0, 'failed': 0}
            modules[module]['total'] += 1
            if test['status'] == 'PASS':
                modules[module]['passed'] += 1
            else:
                modules[module]['failed'] += 1
        
        for module, stats in modules.items():
            success_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            summary_content += f"{module}:\n"
            summary_content += f"  - Total: {stats['total']}\n"
            summary_content += f"  - Passed: {stats['passed']}\n"
            summary_content += f"  - Failed: {stats['failed']}\n"
            summary_content += f"  - Success Rate: {success_rate:.1f}%\n\n"
        
        # Failed tests details
        if failed_tests:
            summary_content += "FAILED TESTS DETAILS:\n"
            summary_content += "=====================\n"
            for test in failed_tests:
                summary_content += f"- {test['test_name']} ({test['module']})\n"
                summary_content += f"  Reason: {test['message']}\n"
                if test.get('screenshot'):
                    summary_content += f"  Screenshot: {test['screenshot']}\n"
                summary_content += "\n"
        
        # Performance insights
        summary_content += "PERFORMANCE INSIGHTS:\n"
        summary_content += "=====================\n"
        summary_content += f"Total execution time: {total_time:.2f} seconds\n"
        if total_time > 120:
            summary_content += "⚠️  Performance Note: Test execution took more than 2 minutes. Consider optimizing.\n"
        else:
            summary_content += "✅ Performance: Test execution within acceptable time frame.\n"
        
        # Save summary file
        summary_path = os.path.join(Config.REPORT_DIR, "test_summary.txt")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"📄 Text summary generated: {summary_path}")
        return summary_path
    
    def generate_html_report(self, test_results, total_time):
        """Generate comprehensive HTML report"""
        passed_tests = [t for t in test_results if t['status'] == 'PASS']
        failed_tests = [t for t in test_results if t['status'] == 'FAIL']
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>E-Commerce Test Suite Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .summary {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .test-result {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .pass {{ background: #d4edda; border: 1px solid #c3e6cb; }}
                .fail {{ background: #f8d7da; border: 1px solid #f5c6cb; }}
                .module-header {{ background: #34495e; color: white; padding: 10px; margin-top: 20px; }}
                .screenshot {{ max-width: 300px; margin: 10px 0; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-card {{ background: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; margin: 0 10px; }}
                .success {{ border-left: 5px solid #28a745; }}
                .warning {{ border-left: 5px solid #ffc107; }}
                .danger {{ border-left: 5px solid #dc3545; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛒 E-Commerce Automated Testing Suite Report</h1>
                <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="stats">
                <div class="stat-card success">
                    <h3>Total Tests</h3>
                    <p style="font-size: 24px; font-weight: bold;">{len(test_results)}</p>
                </div>
                <div class="stat-card success">
                    <h3>Passed</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #28a745;">{len(passed_tests)}</p>
                </div>
                <div class="stat-card danger">
                    <h3>Failed</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #dc3545;">{len(failed_tests)}</p>
                </div>
                <div class="stat-card warning">
                    <h3>Success Rate</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #ffc107;">{(len(passed_tests)/len(test_results)*100 if test_results else 0):.1f}%</p>
                </div>
            </div>
            
            <div class="summary">
                <h2>📊 Test Summary</h2>
                <p><strong>Total Tests:</strong> {len(test_results)}</p>
                <p><strong>Passed:</strong> <span style="color: green">{len(passed_tests)}</span></p>
                <p><strong>Failed:</strong> <span style="color: red">{len(failed_tests)}</span></p>
                <p><strong>Success Rate:</strong> {(len(passed_tests)/len(test_results)*100 if test_results else 0):.1f}%</p>
                <p><strong>Total Time:</strong> {total_time:.2f} seconds</p>
            </div>
            
            <h2>📋 Detailed Test Results</h2>
        """
        
        # Group tests by module
        modules = {}
        for test in test_results:
            module = test['module']
            if module not in modules:
                modules[module] = []
            modules[module].append(test)
        
        for module, tests in modules.items():
            html_content += f'<div class="module-header"><h3>{module}</h3></div>'
            
            for test in tests:
                status_class = "pass" if test['status'] == 'PASS' else "fail"
                status_emoji = "✅" if test['status'] == 'PASS' else "❌"
                
                html_content += f"""
                <div class="test-result {status_class}">
                    <h4>{status_emoji} {test['test_name']}</h4>
                    <p><strong>Status:</strong> {test['status']}</p>
                    <p><strong>Message:</strong> {test['message']}</p>
                    <p><strong>Time:</strong> {test['timestamp']}</p>
                """
                
                if test.get('screenshot'):
                    html_content += f"""
                    <p><strong>Screenshot:</strong></p>
                    <img src="../{test['screenshot']}" alt="Failure Screenshot" class="screenshot">
                    """
                
                html_content += "</div>"
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        report_path = os.path.join(Config.REPORT_DIR, "test_report.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Generate text summary
        self.generate_summary_txt(test_results, total_time)
        
        # Also save JSON report for programmatic access
        json_report = {
            "summary": {
                "total_tests": len(test_results),
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "success_rate": (len(passed_tests)/len(test_results)*100 if test_results else 0),
                "total_time": total_time,
                "generated_at": datetime.now().isoformat()
            },
            "detailed_results": test_results
        }
        
        json_path = os.path.join(Config.REPORT_DIR, "test_report.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2)
        
        print(f"📊 HTML report generated: {report_path}")
        print(f"📄 JSON report generated: {json_path}")