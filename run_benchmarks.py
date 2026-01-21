import os
import sys
import logging
import warnings
import pandas as pd

# Load .env manually
try:
    with open('.env', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                os.environ[key] = value
    print("Loaded .env file.")
except Exception as e:
    print(f"Failed to load .env file: {e}")

# Add current directory to sys.path
sys.path.insert(0, os.path.abspath('.'))

try:
    import abupy
    from abupy import ABuSymbolPd, AbuKLManager, AbuBenchmark, AbuCapital
    from abupy import env as ABuEnv
    from abupy import ABuPickTimeExecute
    from abupy import EMarketTargetType, EMarketSourceType, EMarketDataFetchMode
    from abupy import AbuMetricsBase
    from abupy import AbuFactorBuyBreak
    from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def run_benchmarks():
    print("Starting benchmarks...")
    print(f"Python Version: {sys.version}")
    print(f"Abupy Location: {os.path.dirname(abupy.__file__)}")

    # Suppress warnings for cleaner output
    warnings.filterwarnings('ignore')
    
    # 1. Configure Environment
    # Force Tushare Source
    abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_tushare
    # Force CN Target
    abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_CN
    # Force Network Fetch (to ensure we test API)
    abupy.env.g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_FORCE_NET
    
    # Set Tushare Token from Environment if available (it should be auto-loaded)
    # But let's print if it's loaded
    from abupy.MarketBu.ABuDataFeed import TushareApi
    # TushareApi initializes token in __init__ or lazily?
    # Usually it's global. 
    # Checking ABuEnv.g_project_rom_data_dir might be useful.
    
    # Single process for debugging and log visibility
    n_process = 1
    
    # 2. Select Stocks (CN)
    # 招商银行: 600036, 平安银行: 000001, 万科A: 000002, 工商银行: 601398, 中国石油: 601857
    choice_symbols = ['600036', '000001', '000002', '601398', '601857']
    
    print(f"Testing with symbols: {choice_symbols}")
    
    # 3. Define Strategies
    # Buy Factors
    buy_factors = [
        {'xd': 60, 'class': AbuFactorBuyBreak},
        {'xd': 42, 'class': AbuFactorBuyBreak}
    ]
    
    # Sell Factors
    sell_factors = [
        {'stop_loss_n': 1.0, 'stop_win_n': 3.0, 'class': AbuFactorAtrNStop},
        {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.5},
        {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
    ]
    
    # Benchmark (Base)
    # Using 000300 (沪深300) as benchmark
    # Note: '000300' might need 'sh' prefix or similar depending on implementation,
    # but usually '000300' is recognized as SH index.
    benchmark = AbuBenchmark(benchmark='000300')
    
    # Capital
    capital = AbuCapital(1000000, benchmark)
    
    print("Running Pick Time Execution...")
    try:
        # Initialize KL Manager
        kl_pd_manager = AbuKLManager(benchmark, capital)
        # Pre-fetch data
        kl_pd_manager.batch_get_pick_time_kl_pd(choice_symbols, n_process=n_process)

        orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(
            choice_symbols, benchmark, buy_factors, sell_factors, capital, show=False,
            kl_pd_manager=kl_pd_manager
        )
        
        print("Execution completed.")
        print(f"Orders generated: {len(orders_pd) if orders_pd is not None else 0}")
        
        if orders_pd is not None and not orders_pd.empty:
            print("Orders Head:")
            print(orders_pd.head())
            
            # Metrics
            metrics = AbuMetricsBase(orders_pd, action_pd, capital, benchmark)
            metrics.fit_metrics()
            # metrics.plot_returns_cmp(only_show_returns=True) # Plotting might fail in headless or need setup
            print("Metrics calculated successfully.")
            
            # Print some metrics
            print(f"Algorithm Cumulative Returns: {metrics.algorithm_cum_returns[-1]:.4f}")
            print(f"Benchmark Cumulative Returns: {metrics.benchmark_cum_returns[-1]:.4f}")
        else:
            print("No orders generated. Check data availability or strategy parameters.")
            
    except Exception as e:
        print(f"Runtime Error during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_benchmarks()
