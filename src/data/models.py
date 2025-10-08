"""
============================================================================
DATA MODELS MODULE
============================================================================

Author: Data Analyst Team
Version: 2.0 (Restructured)
Purpose: Define data structures, validation, and type definitions

This module contains:
- Data models and type definitions
- Data validation functions
- Performance categorization logic
- Data quality checks
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import pandas as pd


class PerformanceCategory(Enum):
    """Performance category enumeration for standardized classification"""
    EXCELLENT = "Excellent"
    GOOD = "Good"
    AVERAGE = "Average"
    BELOW_AVERAGE = "Below Average"
    POOR = "Poor"


class Grade(Enum):
    """Employee grade enumeration"""
    SPV = "SPV"  # Supervisor
    S2 = "S2"    # Senior Sales
    DS = "DS"    # Direct Sales


@dataclass
class SalesRecord:
    """Individual sales record data model"""
    area: str
    sub_area: str
    nama: str
    grade: Grade
    target: int
    sales: int
    minus_plus: Optional[int] = None
    percentage: Optional[float] = None
    performance_category: Optional[PerformanceCategory] = None
    
    def __post_init__(self):
        """Calculate derived fields after initialization"""
        self.minus_plus = self.sales - self.target
        self.percentage = round((self.sales / self.target * 100), 2) if self.target > 0 else 0.0
        self.performance_category = self._categorize_performance(self.percentage)
    
    def _categorize_performance(self, percentage: float) -> PerformanceCategory:
        """
        Categorize performance based on achievement percentage
        
        Args:
            percentage: Achievement percentage
            
        Returns:
            PerformanceCategory: Categorized performance level
        """
        if percentage >= 120:
            return PerformanceCategory.EXCELLENT
        elif percentage >= 100:
            return PerformanceCategory.GOOD
        elif percentage >= 80:
            return PerformanceCategory.AVERAGE
        elif percentage >= 60:
            return PerformanceCategory.BELOW_AVERAGE
        else:
            return PerformanceCategory.POOR


@dataclass
class TeamMetrics:
    """Team-level performance metrics"""
    total_team_size: int
    total_target: int
    total_sales: int
    overall_achievement: float
    avg_individual_performance: float
    performance_std: float
    top_performer: str
    top_performance: float
    bottom_performer: str
    bottom_performance: float
    zero_sales_count: int
    excellent_performers: int
    good_performers: int
    needs_improvement: int


@dataclass
class AreaStats:
    """Area-level performance statistics"""
    area: str
    total_target: int
    total_sales: int
    avg_performance: float
    performance_std: float
    team_size: int
    achievement_rate: float


@dataclass
class GradeStats:
    """Grade-level performance statistics"""
    grade: str
    total_target: int
    avg_target: float
    total_sales: int
    avg_sales: float
    avg_performance: float
    performance_std: float
    count: int
    achievement_rate: float


def validate_sales_data(df: pd.DataFrame) -> bool:
    """
    Validate sales data integrity and consistency
    
    Args:
        df: DataFrame containing sales data
        
    Returns:
        bool: True if data is valid, raises exception otherwise
        
    Raises:
        ValueError: If data validation fails
    """
    required_columns = ['Area', 'SubArea', 'Nama', 'Grade', 'Target', 'Sales']
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Check data types and constraints
    if df['Target'].min() <= 0:
        raise ValueError("All targets must be positive")
    
    if df['Sales'].min() < 0:
        raise ValueError("Sales cannot be negative")
    
    if df.isnull().any().any():
        raise ValueError("Data contains null values")
    
    return True


def categorize_performance(percentage: float) -> str:
    """
    Categorize performance based on achievement percentage
    
    Args:
        percentage: Achievement percentage
        
    Returns:
        str: Performance category
    """
    if percentage >= 120:
        return PerformanceCategory.EXCELLENT.value
    elif percentage >= 100:
        return PerformanceCategory.GOOD.value
    elif percentage >= 80:
        return PerformanceCategory.AVERAGE.value
    elif percentage >= 60:
        return PerformanceCategory.BELOW_AVERAGE.value
    else:
        return PerformanceCategory.POOR.value