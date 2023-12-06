"""
Test models.
"""
import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import ProtectedError

from core.models.product import Category, Product, ProductLine, AttributeValue

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    """Tests for the Category model."""

    def test_category_output_str(self, category_factory):
        """Test the __str__ method for the Category model."""
        obj = category_factory()

        assert str(obj) == obj.name

    def test_max_length_for_name(self, category_factory):
        """Test max_length option for the name field."""
        name = "n" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_max_length_for_slug(self, category_factory):
        """Test max_length option for the slug field."""
        slug = "s" * 256
        obj = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_unique_constraint_name(self, category_factory):
        """Test unique constraint for the name field."""
        name = "unique"
        category_factory(name=name)
        with pytest.raises(IntegrityError):
            category_factory(name=name)

    def test_unique_constraint_slug(self, category_factory):
        """Test unique constraint for the slug field."""
        slug = "slug"
        category_factory(slug=slug)
        with pytest.raises(IntegrityError):
            category_factory(slug=slug)

    def test_is_active_false_default(self, category_factory):
        """Test the is_active field set to false by default."""
        obj = category_factory()
        assert obj.is_active is False

    def test_active_custom_queryset(self, category_factory):
        """Test the custom queryset named active
        it's gonna return only active categories."""
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.active().count()
        assert qs == 1

    def test_default_model_manager(self, category_factory):
        """Test the default model manager."""
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.count()
        assert qs == 2

    def test_parent_category_on_delete_protect(self, category_factory):
        """Test on_delete set to protected for the parent field."""
        parent_obj = category_factory()
        category_factory(parent=parent_obj)
        with pytest.raises(IntegrityError):
            parent_obj.delete()

    def test_parent_field_null(self, category_factory):
        """Test the parent field set to null by default."""
        obj = category_factory()
        assert obj.parent is None


class TestProductModel:
    """Tests for the Product model."""

    def test_product_output_str(
            self, product_factory, attribute_value_factory
    ):
        """Test the __str__ method for the Product model."""
        attr_value_obj = attribute_value_factory()
        obj = product_factory(attribute_value=(attr_value_obj,))

        assert str(obj) == obj.name

    def test_max_length_for_name(self, product_factory):
        """Test max_length option for the name field."""
        name = "n" * 231
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_max_length_for_slug(self, product_factory):
        """Test max_length option for the slug field."""
        slug = "s" * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_max_length_for_pid(self, product_factory):
        """Test max_length option for the pid field."""
        pid = "p" * 11
        obj = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_is_digital_false_default(self, product_factory):
        """Test the is_digital field set to false by default."""
        obj = product_factory()
        assert obj.is_digital is False

    def test_delete_category_with_raise_protected_error(
        self, category_factory, product_factory
    ):
        """Test deleting a assigned category
        with raising protected error."""
        category_obj = category_factory()
        product_factory(category=category_obj)
        with pytest.raises(ProtectedError):
            category_obj.delete()

    def test_active_custom_queryset(self, product_factory):
        """Test the custom queryset named active
        it's gonna return only active products."""
        product_factory(pid=1000, is_active=False)
        product_factory(pid=2000, is_active=True)
        qs = Product.objects.active().count()
        assert qs == 1

    def test_default_model_manager(self, product_factory):
        """Test the default model manager."""
        product_factory(is_active=False)
        product_factory(is_active=True)
        qs = Product.objects.count()
        assert qs == 2

    def test_product_type_on_delete_protect(
        self, product_factory, product_type_factory
    ):
        """Test on_delete option set to
        protect for product type field."""
        product_type_obj = product_type_factory()
        product_factory(product_type=product_type_obj)
        with pytest.raises(ProtectedError):
            product_type_obj.delete()


class TestProductLineModel:
    """Test for the ProductLine model."""

    def test_product_line_output_str(
        self, product_line_factory, attribute_value_factory
    ):
        """Test the __str__ method for the ProductLine model."""
        # attribute_value_obj = attribute_value_factory()
        attr_value_obj = attribute_value_factory()
        product_line_obj = product_line_factory(
            attribute_value=(attr_value_obj,)
        )

        assert str(product_line_obj) == product_line_obj.sku

    def test_price_decimal_digits_max_length(self, product_line_factory):
        """Test raises validation error when inserting the
        price field with more than two decimal digits"""
        price = 10.111
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_price_max_digits_length(self, product_line_factory):
        """Test raises validation error when inserting
        the price field with more than five digits."""
        price = 1000.00
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_sku_max_length(self, product_line_factory):
        """Test the max_length option of the sku field."""
        sku = "s" * 11
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_is_active_false_default(self, product_line_factory):
        """Test the is_active field set to false by default."""
        obj = product_line_factory()
        assert obj.is_active is False

    def test_delete_assigned_product_line_with_protected_error(
        self, product_factory, product_line_factory
    ):
        """Test raises protected error while deleting
        assigned product line object to a specific product."""
        prod_obj = product_factory()
        product_line_factory(product=prod_obj)
        with pytest.raises(ProtectedError):
            prod_obj.delete()

    def test_active_custom_queryset(self, product_line_factory):
        """Test the custom queryset named active
        it's gonna return only active product lines."""
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.active().count()
        assert qs == 1

    def test_default_model_manager(self, product_line_factory):
        """Test the default model manager."""
        product_line_factory(is_active=False)
        product_line_factory(is_active=True)
        qs = ProductLine.objects.count()
        assert qs == 2

    def test_duplicate_order_values(
            self, product_line_factory, product_factory
    ):
        """Test preventing from inserting duplicate value for order field."""
        product_obj = product_factory()
        product_line_factory(order=1, product=product_obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=product_obj)

    def test_product_type_on_delete_protect(
        self, product_line_factory, product_type_factory
    ):
        """Test on_delete option set to
        protect for product type field."""
        product_type_obj = product_type_factory()
        product_line_factory(product_type=product_type_obj)
        with pytest.raises(ProtectedError):
            product_type_obj.delete()


class TestProductImageModel:
    """Test for the ProductImage model."""

    def test_product_image_output_str(self, product_image_factory):
        """Test the __str__ method for the ProductImage model."""
        obj = product_image_factory()
        assert str(obj) == f"{obj.product_line.sku}_img"

    def test_max_length_alternative_text(self, product_image_factory):
        """Test the max_length option of the alternative text field."""
        alternative_text = "a" * 101
        with pytest.raises(ValidationError):
            product_image_factory(alternative_text=alternative_text)

    def test_duplicate_order_values(
            self, product_line_factory, product_image_factory
    ):
        """Test preventing from inserting duplicate value for order field."""
        obj = product_line_factory()
        product_image_factory(product_line=obj, order=1)
        with pytest.raises(ValidationError):
            product_image_factory(product_line=obj, order=1)


class TestAttributeModel:
    """Test for the Attribute model."""

    def test_attribute_output_str(self, attribute_factory):
        """Test the __str__ method for the Attribute model."""
        obj = attribute_factory()

        assert str(obj) == obj.name

    def test_max_length_name(self, attribute_factory):
        """Test the max_length option for the name field."""
        name = "n" * 101
        obj = attribute_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_unique_name(self, attribute_factory):
        """Test the unique option for the name field."""
        same_name = "Test"
        attribute_factory(name=same_name)
        with pytest.raises(IntegrityError):
            attribute_factory(name=same_name)


class TestAttributeValueModel:
    """Test for the AttributeValue model."""

    def test_attribute_value_output_str(self, attribute_value_factory):
        """Test the __str__ method for the Attribute model."""
        obj = attribute_value_factory()

        assert str(obj) == f"{obj.attribute}: {obj.value}"

    def test_value_max_length(self, attribute_value_factory):
        """Test the max_length option for the value field."""
        value = "v" * 101
        obj = attribute_value_factory(value=value)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_on_delete_cascade_attribute(
        self, attribute_factory, attribute_value_factory
    ):
        """Test on_delete cascade option for the attribute field."""
        attr_obj = attribute_factory()
        attribute_value_factory(attribute=attr_obj)
        obj = AttributeValue.objects.filter(attribute=attr_obj).exists()
        assert obj is True
        attr_obj.delete()
        obj = AttributeValue.objects.filter(attribute=attr_obj).exists()
        assert obj is False


class TestProductTypeModel:
    """Test for the ProductType model."""

    def test_product_type_output_str(
            self, product_type_factory, attribute_factory
    ):
        """Test the __str__ method for the ProductType model."""
        attr_obj = attribute_factory()
        obj = product_type_factory(attribute=(attr_obj,))

        assert str(obj) == obj.name

    def test_max_length_name(self, product_type_factory):
        """Test the max_length option for the name field."""
        name = "n" * 101
        obj = product_type_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_unique_name(self, product_type_factory):
        """Test unique constraint for the name field."""
        same_name = "Test"
        product_type_factory(name=same_name)
        with pytest.raises(IntegrityError):
            product_type_factory(name=same_name)
