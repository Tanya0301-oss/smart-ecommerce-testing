from modules.functional_testing import FunctionalTesting
from modules.ui_consistency import UIConsistency
from modules.broken_links import BrokenLinksDetector
from modules.performance_snapshot import PerformanceSnapshot
from modules.price_consistency import PriceConsistency
from utils.reporting import ReportGenerator
from config.config import Config
import time

class EcommerceTestSuite:
    def __init__(self):
        Config.setup_directories()
        self.report_generator = ReportGenerator()
        self.test_results = []
        
    def run_full_suite(self):
        """Execute complete test suite"""
        print("🚀 Starting E-Commerce Automated Testing Suite...")
        start_time = time.time()
        
        try:
            # 1. Functional Testing
            print("\n🔧 Running Functional Tests...")
            functional_tester = FunctionalTesting()
            functional_results = functional_tester.run_all_tests()
            self.test_results.extend(functional_results)
            
            # 2. UI Consistency Testing
            print("\n🎨 Running UI Consistency Tests...")
            ui_tester = UIConsistency()
            ui_results = ui_tester.run_all_tests()
            self.test_results.extend(ui_results)
            
            # 3. Broken Links Detection
            print("\n🔗 Running Broken Links Detection...")
            link_checker = BrokenLinksDetector()
            link_results = link_checker.scan_website()
            self.test_results.extend(link_results)
            
            # 4. Performance Testing
            print("\n⚡ Running Performance Tests...")
            performance_tester = PerformanceSnapshot()
            performance_results = performance_tester.measure_performance()
            self.test_results.extend(performance_results)
            
            # 5. Price Consistency Testing
            print("\n💰 Running Price Consistency Tests...")
            price_tester = PriceConsistency()
            price_results = price_tester.run_price_checks()
            self.test_results.extend(price_results)
            
        except Exception as e:
            print(f"❌ Error during test execution: {str(e)}")
        
        finally:
            # Generate comprehensive reports
            total_time = time.time() - start_time
            self.report_generator.generate_html_report(self.test_results, total_time)
            
            # Print final summary to console
            passed = len([t for t in self.test_results if t['status'] == 'PASS'])
            failed = len([t for t in self.test_results if t['status'] == 'FAIL'])
            
            print(f"\n🎯 TEST EXECUTION COMPLETE!")
            print(f"=================================")
            print(f"📊 Total Tests: {len(self.test_results)}")
            print(f"✅ Passed: {passed}")
            print(f"❌ Failed: {failed}")
            print(f"📈 Success Rate: {(passed/len(self.test_results)*100 if self.test_results else 0):.1f}%")
            print(f"⏱️  Total Time: {total_time:.2f} seconds")
            print(f"📄 Reports generated in 'reports/' folder:")
            print(f"   - test_report.html (Detailed HTML report)")
            print(f"   - test_summary.txt (Quick text summary)") 
            print(f"   - test_report.json (Machine-readable data)")
            print(f"📸 Screenshots saved in 'screenshots/' folder")

if __name__ == "__main__":
    test_suite = EcommerceTestSuite()
    test_suite.run_full_suite()