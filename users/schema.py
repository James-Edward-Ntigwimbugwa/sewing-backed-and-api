import graphene
from graphene_django.types import DjangoObjectType
from .models import CustomUser, TailorDetail
from django.contrib.auth.hashers import make_password
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from graphql import GraphQLError

# Configure logging
logger = logging.getLogger(__name__)

# Define the CustomUserType for the GraphQL schema
class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser 
        fields = ("id", "first_name", "last_name", "email", "is_staff", "is_superuser")

# Define TailorDetailType for the TailorDetail model
class TailorDetailType(DjangoObjectType):
    # Add custom fields with camelCase names
    fullName = graphene.String()
    nationalIdNumber = graphene.String()
    phoneNumber = graphene.String()
    areaOfResidence = graphene.String()
    areaOfWork = graphene.String()
    dateOfRegistration = graphene.String()
    isStaff = graphene.Boolean()
    isSuperuser = graphene.Boolean()
    
    class Meta:
        model = TailorDetail
        fields = ("id", "username", "email", "sex")
    
    def resolve_fullName(self, info):
        return self.full_name
    
    def resolve_nationalIdNumber(self, info):
        return self.national_id_number
    
    def resolve_phoneNumber(self, info):
        return self.phone_number
    
    def resolve_areaOfResidence(self, info):
        return self.area_of_residence
    
    def resolve_areaOfWork(self, info):
        return self.area_of_work
    
    def resolve_dateOfRegistration(self, info):
        return self.date_of_registration.isoformat() if self.date_of_registration else None
    
    def resolve_isStaff(self, info):
        return self.is_staff
    
    def resolve_isSuperuser(self, info):
        return self.is_superuser

# Define the mutation class for creating a CustomUser
class CreateCustomUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    custom_user = graphene.Field(CustomUserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, first_name, last_name, email, password):
        try:
            logger.debug(f"Creating user: {first_name} {last_name} with email: {email}")
            
            # Check if user already exists
            if CustomUser.objects.filter(email=email).exists():
                return CreateCustomUser(
                    custom_user=None,
                    success=False,
                    message="User with this email already exists"
                )

            # Create user using the manager for proper setup
            custom_user = CustomUser.objects.create_user(
                email=email,
                password=password,  # The create_user method will hash the password
                first_name=first_name,
                last_name=last_name
            )
            
            logger.info(f"User created successfully: {custom_user.email}")
            return CreateCustomUser(
                custom_user=custom_user,
                success=True,
                message="User created successfully"
            )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return CreateCustomUser(
                custom_user=None,
                success=False,
                message=f"Error creating user: {str(e)}"
            )

# Define the customer user login mutation
class CustomerUserLogin(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    token = graphene.String()
    refresh = graphene.String()
    user = graphene.Field(CustomUserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, password):
        try:
            logger.debug(f"Attempting customer login with email: {email}")
            
            # Try to authenticate the customer user
            user = authenticate(username=email, password=password)
            
            if user is None or not isinstance(user, CustomUser):
                logger.warning(f"Customer authentication failed for email: {email}")
                return CustomerUserLogin(
                    token=None,
                    refresh=None,
                    user=None,
                    success=False,
                    message="authentication failed. "
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            logger.info(f"Customer authentication successful for: {user.email}")
            
            return CustomerUserLogin(
                token=str(refresh.access_token),
                refresh=str(refresh),
                user=user,
                success=True,
                message="Authentification successful"
            )
        except Exception as e:
            logger.error(f"Error during customer authentication: {str(e)}")
            return CustomerUserLogin(
                token=None,
                refresh=None,
                user=None,
                success=False,
                message=f"Error during authentication: {str(e)}"
            )

# Define the mutation class for obtaining JWT tokens
class ObtainJwtToken(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    token = graphene.String()
    refresh = graphene.String()
    user = graphene.Field(CustomUserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, password):
        try:
            logger.debug(f"Attempting to obtain token for email: {email}")
            
            # Use authenticate with correct parameters
            user = authenticate(username=email, password=password)
            
            if user is None:
                logger.warning(f"Authentication failed for email: {email}")
                return ObtainJwtToken(
                    token=None,
                    refresh=None,
                    user=None,
                    success=False,
                    message="Login failed. Please try againInvalid credentials"
                )

            refresh = RefreshToken.for_user(user)
            logger.info(f"Authentication successful for user: {user.email}")
            
            return ObtainJwtToken(
                token=str(refresh.access_token),
                refresh=str(refresh),
                user=user,
                success=True,
                message="Login successful"
            )
        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
            return ObtainJwtToken(
                token=None,
                refresh=None,
                user=None,
                success=False,
                message=f"Error during authentication: {str(e)}"
            )

# Define the mutation for tailor login
class TailorLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    
    token = graphene.String()
    refresh = graphene.String()
    tailor = graphene.Field(TailorDetailType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username, password):
        try:
            # Input validation and cleaning
            if not username or not password:
                logger.warning("Authentication attempt with empty username or password")
                return TailorLogin(
                    token=None,
                    refresh=None,
                    tailor=None,
                    success=False,
                    message="Username and password are required"
                )
            
            # Clean and normalize the username
            cleaned_username = username.strip().rstrip('@').lower()
            
            if not cleaned_username:
                logger.warning("Authentication attempt with invalid username after cleaning")
                return TailorLogin(
                    token=None,
                    refresh=None,
                    tailor=None,
                    success=False,
                    message="Invalid username format"
                )
            
            logger.debug(f"Login attempt for user '{cleaned_username}' (original: '{username}')")
            
            # Step 1: Check if tailor exists
            try:
                tailor = TailorDetail.objects.get(username__iexact=cleaned_username)
                logger.debug(f"User '{cleaned_username}' found in database")
            except TailorDetail.DoesNotExist:
                logger.warning(f"User '{cleaned_username}' not found in tailor records")
                return TailorLogin(
                    token=None,
                    refresh=None,
                    tailor=None,
                    success=False,
                    message="Invalid username or password"  # Generic message for security
                )
            
            # Step 2: Check if account is active (if you have this field)
            if hasattr(tailor, 'is_active') and not tailor.is_active:
                logger.warning(f"Login attempt for inactive user '{cleaned_username}'")
                return TailorLogin(
                    token=None,
                    refresh=None,
                    tailor=None,
                    success=False,
                    message="Account is inactive"
                )
            
            # Step 3: Authenticate password
            if hasattr(tailor, 'check_password'):
                # If TailorDetail has password checking method
                password_valid = tailor.check_password(password)
            else:
                # Fallback to Django's authenticate
                authenticated_user = authenticate(username=cleaned_username, password=password)
                password_valid = authenticated_user is not None and authenticated_user == tailor
            
            if not password_valid:
                logger.warning(f"Invalid password for user '{cleaned_username}'")
                return TailorLogin(
                    token=None,
                    refresh=None,
                    tailor=None,
                    success=False,
                    message="Invalid username or password"  # Generic message for security
                )
            
            # Step 4: Generate tokens
            try:
                refresh = RefreshToken.for_user(tailor)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                logger.info(f"Authentication successful for user '{tailor.username}'")
                
                return TailorLogin(
                    token=access_token,
                    refresh=refresh_token,
                    tailor=tailor,
                    success=True,
                    message=f"Welcome back, {tailor.username}!"
                )
                
            except Exception as token_error:
                logger.error(f"Token generation failed for user '{cleaned_username}': {str(token_error)}")
                return TailorLogin(
                    token=None,
                    refresh=None,
                    tailor=None,
                    success=False,
                    message="Authentication service temporarily unavailable"
                )
            
        except Exception as e:
            logger.error(f"Unexpected error during authentication for user '{username}': {str(e)}", exc_info=True)
            return TailorLogin(
                token=None,
                refresh=None,
                tailor=None,
                success=False,
                message="An unexpected error occurred during authentication"
            )

# Define a mutation to register TailorDetail
class RegisterTailor(graphene.Mutation):
    tailor = graphene.Field(TailorDetailType)
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        fullName = graphene.String(required=True)  # Changed from full_name to fullName
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        nationalIdNumber = graphene.String(required=True)  # Changed from national_id_number
        phoneNumber = graphene.String(required=True)  # Changed from phone_number
        sex = graphene.String(required=True)
        areaOfResidence = graphene.String(required=True)  # Changed from area_of_residence
        areaOfWork = graphene.String(required=True)  # Changed from area_of_work
        password = graphene.String(required=True)
        
    def mutate(self, info, fullName, username, email, nationalIdNumber, phoneNumber, 
               sex, areaOfResidence, areaOfWork, password):
        try:
            # Validate inputs
            if TailorDetail.objects.filter(username=username).exists():
                return RegisterTailor(
                    tailor=None,
                    success=False,
                    message="Username already exists"
                )
               
            if TailorDetail.objects.filter(email=email).exists():
                return RegisterTailor(
                    tailor=None,
                    success=False,
                    message="Email already exists"
                )
            
            # Create tailor using the manager for proper setup
            tailor = TailorDetail.objects.create_user(
                username=username,
                full_name=fullName,  # Map camelCase to snake_case for model
                national_id_number=nationalIdNumber,
                phone_number=phoneNumber,
                email=email,
                sex=sex,
                area_of_residence=areaOfResidence,
                area_of_work=areaOfWork,
                password=password  # Manager will hash the password
            )
            
            logger.info(f"Tailor registered successfully: {tailor.username}")
            return RegisterTailor(
                tailor=tailor,
                success=True,
                message="Tailor registered successfully"
            )
        except Exception as e:
            logger.error(f"Error during tailor registration: {str(e)}")
            return RegisterTailor(
                tailor=None,
                success=False,
                message=f"Error during registration: {str(e)}"
            )

# Define the Query class
class Query(graphene.ObjectType):
    all_custom_users = graphene.List(CustomUserType)
    all_tailors = graphene.List(TailorDetailType)
    custom_user = graphene.Field(CustomUserType, id=graphene.ID())
    tailor = graphene.Field(TailorDetailType, id=graphene.ID())

    def resolve_all_custom_users(self, info):
        logger.debug("Fetching all custom users.")
        return CustomUser.objects.all()
    
    def resolve_all_tailors(self, info):
        logger.debug("Fetching all registered tailors.")
        return TailorDetail.objects.all()
    
    def resolve_custom_user(self, info, id):
        try:
            return CustomUser.objects.get(pk=id)
        except CustomUser.DoesNotExist:
            return None
    
    def resolve_tailor(self, info, id):
        try:
            return TailorDetail.objects.get(pk=id)
        except TailorDetail.DoesNotExist:
            return None

# Define the main Mutation class
class Mutation(graphene.ObjectType):
    create_custom_user = CreateCustomUser.Field()
    obtain_jwt_token = ObtainJwtToken.Field()
    register_tailor = RegisterTailor.Field()
    tailor_login = TailorLogin.Field()
    customer_user_login = CustomerUserLogin.Field()  # Add the new customer login mutation

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)